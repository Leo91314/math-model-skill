# 数学建模项目环境模板

复制到新建空项目目录后，执行 `uv sync --locked` 创建Python 3.12环境。原依赖清单、uv锁文件和带哈希requirements均保留；不复制原机虚拟环境。

```bash
uv sync --locked
bash scripts/check_env.sh
```

默认只运行合成数据科学计算演示及本地Jupyter核验证。使用 `bash scripts/check_env.sh --documents` 进一步生成中文DOCX、LaTeX和PDF；需要XeLaTeX与pdftoppm。

Word页面渲染另依赖已授权的Documents插件。将插件目录通过 `CODEX_DOCS_SKILL` 提供，必要时用 `CODEX_DOCS_PYTHON` 指定对应Python。没有提供时明确跳过Word渲染，不宣称文档页面通过检查。

LaTeX使用Fandol字体；Word部分保留原Mac中文字体与Fontconfig回退方案，换系统时按实际字体配置。此模板来自已运行过的旧环境，但整理版不代表已在所有平台重新验证。

建议目录：原件 `problem/`、原始数据 `data/raw/`、处理数据 `data/processed/`、代码 `src/`、结果 `outputs/`、论文 `paper/`。演示全部位于 `outputs/env_check/`，不能作为赛题结果。
