"""Start and shut down the project-local Jupyter kernel after an actual calculation."""

import json
import tempfile
from pathlib import Path

from jupyter_client import KernelManager

ROOT = Path(__file__).resolve().parents[1]
ipc_dir = tempfile.TemporaryDirectory(prefix="math-kernel-")
manager = KernelManager(kernel_name="math-model-skill", transport="ipc", ip=ipc_dir.name + "/kernel")
manager.start_kernel(cwd=str(ROOT))
client = manager.blocking_client()
client.start_channels()
try:
    client.wait_for_ready(timeout=30)
    code = (
        "import sys, numpy as np\n"
        f"assert sys.prefix == {str(ROOT / '.venv')!r}\n"
        "assert np.isclose(np.linalg.det([[2., 0.], [0., 3.]]), 6.)\n"
        "print('Project Jupyter kernel calculation passed.')\n"
    )
    reply = client.execute_interactive(code, timeout=30)
    assert reply["content"]["status"] == "ok", reply["content"]
finally:
    client.stop_channels()
    manager.shutdown_kernel(now=True)
    ipc_dir.cleanup()

report_path = ROOT / "outputs" / "env_check" / "environment_report.json"
report = json.loads(report_path.read_text())
report["jupyter_kernel"] = "passed; local math-model-skill kernel started, calculated and shut down"
report_path.write_text(json.dumps(report, indent=2) + "\n")
