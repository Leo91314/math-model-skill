"""A small reproducible environment check. All data are explicitly synthetic."""
# ruff: noqa: E402 -- Select a writable cache and headless backend before pyplot imports.

import json
import os
import platform
import sys
import tomllib
from datetime import datetime, timezone
from importlib import import_module, metadata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "env_check"
OUT.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".cache" / "matplotlib"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares, linprog


def temperature(t, k):
    """Newton cooling ODE, time in minutes and temperature in Celsius."""
    solution = solve_ivp(
        lambda _t, y: -k * (y - 20),
        (0, float(np.max(t))),
        [80.0],
        t_eval=np.asarray(t),
        rtol=1e-9,
        atol=1e-11,
    )
    if not solution.success:
        raise RuntimeError(solution.message)
    return solution.y[0]


def main():
    seed = 20260910
    rng = np.random.default_rng(seed)
    t = np.linspace(0, 30, 61)
    truth = temperature(t, 0.12)
    pd.DataFrame(
        {"time_min": t, "temperature_C": truth + rng.normal(0, 0.25, t.size)}
    ).to_csv(OUT / "synthetic_cooling.csv", index=False)
    data = pd.read_csv(OUT / "synthetic_cooling.csv")
    fit = least_squares(
        lambda p: temperature(data.time_min.to_numpy(), p[0]) - data.temperature_C,
        [0.08],
        bounds=([0.001], [1.0]),
    )
    fitted_k = float(fit.x[0])
    ode_error = float(np.max(np.abs(truth - (20 + 60 * np.exp(-0.12 * t)))))
    assert fit.success and abs(fitted_k - 0.12) < 0.005
    assert ode_error < 1e-6
    # Synthetic resource allocation: maximize 3x+2y with x+y<=4, x<=2.
    lp = linprog([-3, -2], A_ub=[[1, 1], [1, 0]], b_ub=[4, 2], method="highs")
    assert lp.success and np.allclose(lp.x, [2, 2]) and abs(lp.fun + 10) < 1e-8

    import cvxpy as cp
    import highspy
    import networkx as nx
    import simpy
    import statsmodels.api as sm
    import sympy as sp
    from pymoo.algorithms.moo.nsga2 import NSGA2
    from pymoo.optimize import minimize
    from pymoo.problems import get_problem
    from SALib.analyze import sobol as sobol_analyze
    from SALib.sample import sobol as sobol_sample
    from sklearn.linear_model import LinearRegression

    integer_x = cp.Variable(2, integer=True)
    mip = cp.Problem(cp.Maximize(np.array([3, 2]) @ integer_x), [
        integer_x >= 0, cp.sum(integer_x) <= 4, integer_x[0] <= 2,
    ])
    mip.solve(solver="HIGHS")
    assert mip.status == "optimal" and np.allclose(integer_x.value, [2, 2])
    q = cp.Variable(2)
    qp = cp.Problem(cp.Minimize(cp.sum_squares(q - [2, 1])), [q >= 0, cp.sum(q) == 1])
    qp.solve(solver="CLARABEL")
    assert qp.status == "optimal" and np.allclose(q.value, [1, 0], atol=1e-3)
    sym_t = sp.Symbol("t")
    assert sp.simplify(sp.diff(20 + 60 * sp.exp(-sym_t), sym_t) + 60 * sp.exp(-sym_t)) == 0
    train_x = np.arange(10).reshape(-1, 1)
    train_y = 3 * train_x[:, 0] + 2
    assert np.allclose(LinearRegression().fit(train_x, train_y).coef_, [3])
    assert np.allclose(sm.OLS(train_y, sm.add_constant(train_x)).fit().params, [2, 3])
    assert nx.shortest_path_length(nx.path_graph(5), 0, 4) == 4
    queue = simpy.Environment()
    server = simpy.Resource(queue, capacity=1)
    departures = []

    def customer():
        with server.request() as request:
            yield request
            yield queue.timeout(2)
            departures.append(queue.now)

    queue.process(customer())
    queue.process(customer())
    queue.run()
    assert departures == [2, 4]
    problem = {"num_vars": 2, "names": ["x1", "x2"], "bounds": [[0, 1], [0, 1]]}
    samples = sobol_sample.sample(problem, 256, calc_second_order=False, seed=seed)
    sensitivity = sobol_analyze.analyze(
        problem, samples[:, 0] + 2 * samples[:, 1], calc_second_order=False, seed=seed
    )
    assert np.allclose(sensitivity["S1"], [0.2, 0.8], atol=0.04)
    pareto = minimize(get_problem("zdt1"), NSGA2(pop_size=40), ("n_gen", 20), seed=seed)
    assert pareto.F.ndim == 2 and pareto.F.shape[1] == 2 and np.isfinite(pareto.F).all()
    data.to_excel(OUT / "synthetic_cooling.xlsx", index=False)
    assert np.allclose(pd.read_excel(OUT / "synthetic_cooling.xlsx"), data)

    modules = {
        "scikit-learn": "sklearn", "python-docx": "docx", "pymupdf": "pymupdf",
        "SALib": "SALib", "ruff": None,
    }
    versions = {}
    dependencies = tomllib.loads((ROOT / "pyproject.toml").read_text())["project"]["dependencies"]
    for requirement in dependencies:
        name = requirement.split(">=")[0]
        module_name = modules.get(name, name.replace("-", "_"))
        if module_name:
            import_module(module_name)
        versions[name] = metadata.version(name)

    fig, ax = plt.subplots(figsize=(7.0, 4.1), layout="constrained")
    ax.scatter(data.time_min, data.temperature_C, s=17, color="#436a85", label="Synthetic data")
    ax.plot(t, temperature(t, fitted_k), color="#bd5628", label="ODE fit")
    ax.set(xlabel="Time (min)", ylabel="Temperature (C)", title="Environment check: synthetic cooling")
    ax.legend(frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    fig.savefig(OUT / "synthetic_cooling.png", dpi=180)
    fig.savefig(OUT / "synthetic_cooling.svg")
    plt.close(fig)
    results = {
        "data_origin": "SYNTHETIC ENVIRONMENT TEST ONLY; not contest data or findings",
        "seed": seed,
        "sample_count": len(data),
        "true_k_per_min": 0.12,
        "fitted_k_per_min": fitted_k,
        "ode_max_abs_error_C": ode_error,
        "fit_rmse_C": float(np.sqrt(np.mean(fit.fun**2))),
        "linear_program_solution": lp.x.tolist(),
        "linear_program_maximum": float(-lp.fun),
        "core_status": "passed",
        "mixed_integer_program": {"solver": "HIGHS", "solution": integer_x.value.tolist()},
        "quadratic_program": {"solver": "CLARABEL", "solution": q.value.tolist()},
        "sobol_first_order": sensitivity["S1"].tolist(),
        "nsga2_returned_points": int(len(pareto.F)),
        "simpy_departure_times": departures,
        "extended_status": "passed",
    }
    (OUT / "results.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    report = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "Synthetic environment check; no contest model or data supplied.",
        "python": sys.version,
        "executable": sys.executable,
        "base_prefix": sys.base_prefix,
        "platform": platform.platform(),
        "architecture": platform.machine(),
        "packages": versions,
        "cvxpy_solvers": cp.installed_solvers(),
        "highs_version": highspy.Highs().version(),
        "numerical_checks": "passed",
        "artifacts": "not_yet_checked",
        "limitations": [
            "Tests use small synthetic problems, not competition-size workloads.",
            "Use the project Python 3.12 environment; record its actual base interpreter.",
            "No GPU or commercial solver is required or tested.",
        ],
    }
    (OUT / "environment_report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
