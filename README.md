# math model skill

从读懂题目到完成论文的一套数学建模 AI 工作资料。

核心是自主设计的七步技能：**读题 → 检索 → 讨论 → 设计 → 执行 → 成稿 → 质询**。重视题意到目标的合理转化、最小真实计算、有依据的结论，以及围绕中心发现组织论文。

本仓库整理原创七步、BZD与科学计算技能、绘图写作工具、提示词和空白模板。当前为私有资料库；各资源的作者与授权分别保留，见 [来源与授权](NOTICE.md)。

## 七步核心

| 步骤 | 调用名 | 用途 |
|---|---|---|
| 1 | `math-model-skill1-read` | 完整读题，区分事实、推论、假设与歧义，明确逐问目标 |
| 2 | `math-model-skill2-research` | 查原始资料，比较可行模型、机理与算法 |
| 3 | `math-model-skill3-debate` | 围绕用户真实理解讨论模型、主张与证据 |
| 4 | `math-model-skill4-design` | 设计有判断力的计算、对照和评价方式 |
| 5 | `math-model-skill5-execute` | 完成代码、真实计算、验证和图表 |
| 6 | `math-model-skill6-refine` | 根据实际结果成稿、修订并打磨论证主线 |
| 7 | `math-model-skill7-rebuttal` | 内部模拟评阅，定位关键质疑与最小补证 |

七步可以往返，也可以从已有成果对应的步骤开始。第5步交计算与图表，第6步写论文；已有授权按实际缺口衔接。

## 安装与使用

克隆后，只安装原创七步到指定项目：

```bash
gh repo clone Leo91314/math-model-skill
cd math-model-skill
python3 scripts/install_skills.py --project /path/to/your-project
```

`--group project` 安装七步与原项目18个第三方技能，共25个；`--group all` 加上10个本机配套技能，共35个。已有同名目录会跳过，安装器不改全局配置。

在目标项目打开Codex后可用：

```text
使用 $math-model-skill1-read，完整阅读题目和附件说明。
解释研究对象与各问任务，区分事实、推论、假设和歧义；
明确输入、目标、硬约束、单位、问间继承及交付物。
本次只读题，不提前选择模型。
```

完整调用见 [七步提示词](prompts/seven-stage-prompts.md)、[工作流指南](docs/workflow-guide.md)；原项目名称的变化见 [名称对照](docs/name-mapping.md)。本地发现目录与手动调用方式参考 [OpenAI官方技能文档](https://learn.chatgpt.com/docs/build-skills)。

## 资料入口

| 内容 | 入口 |
|---|---|
| 35个现行技能与来源 | [技能目录](docs/skill-catalog.md) |
| 题意转为数学任务 | [问题定义模板](templates/problem-definition.md) |
| 论文的问题提出与分析 | [分析写作模板](templates/problem-analysis.md) |
| 模型假设 | [假设模板](templates/model-assumptions.md) |
| 主张与证据对应 | [证据卡](templates/evidence-card.md) |
| 真实计算与复现记录 | [计算记录模板](templates/reproducibility.md) |
| AI使用记录 | [CSV空表](templates/ai-usage-log.csv) |
| 中文LaTeX空白论文 | [LaTeX模板](templates/latex-cumcm-2026/README.md) |
| Python依赖、合成环境演示 | [项目环境模板](templates/project/README.md) |
| 环境提醒与语法检查hooks | [Hooks示例](templates/hooks/README.md) |
| Word、表格、插件版PDF等 | [外部技能入口](docs/external-skills.md) |
| 旧版16入口与原提示词 | [历史归档](archives/README.md) |
| 整理范围与修改 | [整理说明](docs/collection-notes.md) |

## 复用科学计算环境

在一个新建空目录中复制 `templates/project/` 的内容，再恢复依赖：

```bash
uv sync --locked
```

依赖是原项目保存的Python 3.12环境快照，虚拟环境需要在新机器重新创建。环境演示全部使用合成数据；安装技能本身不会运行演示、模型或联网任务。

原项目25个技能不等于25项都用于赛题；本机配套目录也可能比当时使用的版本更新。历史验证只代表其标明的版本和任务范围。2026比赛规则和排版配置为历史参考，正式使用需核对当届原文。
