# 数学建模 A 题工作区

本目录为题目发布前的本地准备环境。题目到手后，把原始题面放入 `problem/`、附件放入 `data/raw/`，在这个 Codex 项目中继续发给我即可。当前演示全部使用合成数据，不代表已知赛题或比赛结论。

按阶段复制使用的提示词与补充技能建议见 [数模提示词](docs/数模提示词.md)。

已新增 **Liminghao 15 步数模技能 + 1 个总控**，可以直接说：“使用 `$liminghao-skill1-read` 帮我读题并理解。”完整调用名、示例和阶段产出见 [Liminghao Skills 使用指南](docs/liminghao-skills使用指南.md)，实际测试见 [验证报告](outputs/liminghao_skills_validation/验证报告.md)。

## 现在可以用什么

- **34 个项目技能**：Liminghao 自定义 16 个、BZD 数模社 12 个、K-Dense 科学计算 6 个，位于 `.agents/skills/`。第三方技能固定版本安装，保留来源和许可声明。
- **独立 Python 3.12 环境**：数值计算、优化、仿真、统计、机器学习、灵敏度分析、Excel、Word、PDF 与 Jupyter。
- **中文文档链路**：已有 XeLaTeX、Pandoc、LibreOffice 和 PDF 渲染工具；环境示例在 `outputs/env_check/`。
- **项目 hooks**：启动/恢复时提示环境入口；结束时检查项目 Python 语法并保存摘要。自动运行需要在 Codex 中审阅信任，见下文。

已有的 planning-with-files、LaTeX、PDF、Word、表格、Jupyter、学术写作和绘图技能继续可用，无需重复安装。Codex 运行时已确认 34 个项目技能可发现；当前任务列表未刷新时，重新打开该项目任务或按完整 SKILL.md 路径调用。

## 计算与一键检查

在终端进入本项目后：

```bash
cd '.'
bash scripts/check_env.sh
```

该命令运行合成 CSV → 常微分方程 → 参数拟合 → 约束优化 → 图表 → 中文 PDF/Word，并验证本地 Jupyter 内核。结果写入 `outputs/env_check/`；不下载依赖或调用付费模型。脚本会重建该演示目录中的输出文件。

最终已从项目外目录完整执行成功。若从 Codex 受限沙箱运行，Jupyter 的本地 socket 启动需要工具侧授权；普通本机终端可直接运行。验证使用小规模合成问题，不代表已验证未知赛题的大规模计算负载。

执行自己的求解程序：

```bash
.venv/bin/python src/solve.py
```

`src/solve.py` 是将来求解脚本的示例名称，题目未发布时尚不存在。当前系统 `python3` 没有科学计算包，务必使用 `.venv/bin/python`。

打开 Jupyter：

```bash
.venv/bin/jupyter lab
```

选择 `Python 数学建模A (.venv)` 内核。该内核安装在项目 `.venv`，不会替换全局内核。

主依赖包括 NumPy、SciPy、pandas、SymPy、Matplotlib、Seaborn、scikit-learn、statsmodels、CVXPY、HiGHS、Pymoo、SimPy、SALib、NetworkX、openpyxl、python-docx、PyMuPDF、JupyterLab 和 Ruff。完整版本见 `uv.lock` 与 `requirements.lock.txt`。

如需恢复依赖，使用现有 uv：

```bash
UV_CACHE_DIR="$PWD/.uv-cache" uv sync --locked
```

恢复依赖可能联网；平时计算和一键检查不需要联网。`.venv` 当前基于本机 `/opt/homebrew/anaconda3` 的 Python 3.12.7，移动项目或删除这个解释器后需要重建环境。文档渲染还依赖本机 TeX、LibreOffice 和 Codex 文档运行时，不能把 `.venv` 单独复制到另一台机器就当作完整环境。

## Skills 清单与调用

日常按步骤解题或写论文，可使用 [Liminghao 系列](docs/liminghao-skills使用指南.md)。总控 `$liminghao-skill0-workflow` 根据已有进度连续推进；指定分步只完成该步，不要求补齐所有前序报告。下面的原有专业技能继续按需提供补充能力。

| 任务 | 技能 |
|---|---|
| 读题与拆解 | bzd-problem-translator、bzd-modeling-ideas |
| 流程与模型适配 | bzd-modeling-workflow、bzd-model-dictionary |
| 求解与假设核对 | bzd-model-solution-checker、bzd-model-assumption-checker |
| 论文内容检查 | bzd-problem-restatement、bzd-problem-analysis-checker、bzd-abstract-checker、bzd-symbol-notation-checker |
| 引用、附录、真实 AI 使用记录 | bzd-reference-appendix-checker、bzd-ai-usage-disclosure |
| 符号推导、多目标优化、离散仿真 | sympy、pymoo、simpy |
| 统计诊断、图论、机器学习 | statsmodels、networkx、scikit-learn |

可以直接用中文描述需求，也可以明确写 `$bzd-problem-translator` 或 `$sympy`。按实际任务选择技能，不需要逐一启动。安装来源：

- [BZD 原作者仓库](https://github.com/BZDmathclub/bzd-math-modeling-skills)：查询时 238 stars；安装提交 `332d55c2f3244c9e193e90749f42bcc0d534ce53`。模型字典保留“BZD数模社制作”及非商业许可声明。
- [K-Dense Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills)：查询时 44,174 stars；安装提交 `9cf7d9aea7d84754db4c167ab04b299d33c444bc`。保留 MIT 许可；移除自动给技能项目添加论文引用的指令，并修正 SimPy 本地路径。

stars 为 2026-09-10 查询快照，衡量的是仓库关注度。没有安装 BZD 的 AI 文风检测、主观格式评分、综合获奖预测和高校奖项预测模块。来源、改动与校验记录见 `docs/skills-manifest.json`、`docs/skill-adaptations.patch` 和 `docs/skill-validation.json`。

## Hooks 的最后一步

配置在 `.codex/hooks.json`，脚本在 `tools/workspace_hook.py`。这两个 hooks 均已通过手动验证：

1. **SessionStart**：提示项目解释器、README、AGENTS 和续接记录位置，也适用于压缩上下文后的恢复。
2. **Stop**：对 `src/`、`scripts/`、`tools/` 的 Python 文件进行语法解析，写入 `outputs/last_hook_check.json`。语法有错会提示，仍允许结束；不会执行代码或证明模型结果正确。

**要启用自动触发**：在该目录运行 `codex`，输入 `/hooks`，审阅并信任这两项。项目的 `.codex` 配置层也需要处于已信任状态。新建或修改 hook 后，Codex 要求对确切定义重新审阅；这是 [Codex 官方 hooks 机制](https://learn.chatgpt.com/docs/hooks)的要求。此项目没有改写信任记录，没有关闭审批，也没有替换全局通知。

不启用 hooks 也能正常读题、计算和生成论文；可随时手动运行一键检查。

## 题目到手后的目录

```text
problem/          原始题面与官方说明
data/raw/         原始附件
data/processed/   清洗后数据
src/              求解和验证代码
outputs/          图、表、结果；env_check 子目录仅用于环境演示
paper/            正式论文源文件
scripts/          环境检查与文档输出脚本
docs/             技能来源和环境准备记录
```

先读全题和数据，明确各问输出、单位、约束及验证方式，再跑通一个可解释的基线。比赛规则、论文版式和 AI 使用披露要求在拿到当届官方文件后核对；不预先假定“A题”的模型类型。
