---
name: liminghao-skill0-workflow
description: 按现有成果和结构线索调度 Liminghao 数模流程，支持探索、计算与写作往返。用于全题推进、续接或判断下一步；单项任务调用相应分步技能。
---

# 数模全流程总控

目标是交付题意覆盖完整、有方法洞察、结果可核查、论证清楚的参赛论文。步骤编号用于定位能力，不规定研究顺序；根据已有证据和有价值的结构线索选择下一项实际工作。

首次使用本系列时读 [共同约定](references/principles.md)。从用户请求、当前材料和项目记录确定这次范围。已经明确的比赛、题目、路径、输出偏好和授权直接沿用。

## 选择下一步
按可检查的事实判断状态，而不是仅听取“已经建好模型”等标签：题目是否齐全、核心公式是否清楚、是否有真实运行输出、输出是否通过关键约束检查、论文是否对应当前结果。

| 步骤 | 技能 | 什么时候使用 | 最小可用成果 |
|---|---|---|---|
| 1 读题 | [liminghao-skill1-read](../liminghao-skill1-read/SKILL.md) | 原题初读、条件或交付物不清 | 有来源的逐问任务清单 |
| 2 转化 | [liminghao-skill2-analyze](../liminghao-skill2-analyze/SKILL.md) | 从题意到数学对象 | 变量、目标、约束与跨问关系 |
| 3 数据 | [liminghao-skill3-data](../liminghao-skill3-data/SKILL.md) | 文件/数据质量会影响路线 | 可计算输入及处理依据 |
| 4 调研 | [liminghao-skill4-research](../liminghao-skill4-research/SKILL.md) | 有明确知识或参数缺口 | 原始来源及适用性结论 |
| 5 主线 | [liminghao-skill5-plan](../liminghao-skill5-plan/SKILL.md) | 需要选整体路线与先后顺序 | 基线、扩展与验证路线 |
| 6 建模 | [liminghao-skill6-model](../liminghao-skill6-model/SKILL.md) | 需要可实现的数学关系 | 方程、假设、参数及条件 |
| 7 基线 | [liminghao-skill7-baseline](../liminghao-skill7-baseline/SKILL.md) | 缺真实端到端运行 | 可运行入口与真实基线 |
| 8 基础检查 | [liminghao-skill8-check](../liminghao-skill8-check/SKILL.md) | 刚得到基线或明显异常 | 单位、边界、残差/特例检查 |
| 9 全题求解 | [liminghao-skill9-solve](../liminghao-skill9-solve/SKILL.md) | 基线可靠但各问未覆盖 | 相互一致的全题结果 |
| 10 探索/改进 | [liminghao-skill10-improve](../liminghao-skill10-improve/SKILL.md) | 有待查证结构猜想或具体瓶颈，可在基线前 | 猜想去留依据，或同口径改进证据 |
| 11 验证 | [liminghao-skill11-validate](../liminghao-skill11-validate/SKILL.md) | 核心结论需更强依据 | 收敛、可行性、稳健性等所需证据 |
| 12 解释 | [liminghao-skill12-interpret](../liminghao-skill12-interpret/SKILL.md) | 有结果但意义和主线不清 | 中心发现及可信边界 |
| 13 正文 | [liminghao-skill13-write](../liminghao-skill13-write/SKILL.md) | 写正文、修改初稿 | 以证据组织的论文 |
| 14 摘要 | [liminghao-skill14-abstract](../liminghao-skill14-abstract/SKILL.md) | 标题/摘要/关键词定稿 | 自足且与正文一致的摘要 |
| 15 交付 | [liminghao-skill15-submit](../liminghao-skill15-submit/SKILL.md) | 全文审查与提交包准备 | 核对过的最终文件 |

## 推进方式
1. 用几句话说明当前最影响进度的问题和本次将完成的成果，随后读取并执行对应技能。只加载这次实际需要的技能及参考文件。
2. 只有原题时，先理解任务并留意结构线索。已有可实现关系时直接做基线；有望改变表示或降低计算负担的猜想时，可先用plan安排或improve执行一个小验证，不等待全题解完。有验证结果时可直接写相应章节。
3. 用户要求“从读题做到基线”，完成相关阶段而不自动扩成全文；用户要求“完成论文”，在已有授权内继续，直到论文及所需支撑成果完成或出现确需用户补充的关键缺口。用户只问“下一步是什么”，交判断即可，不擅自启动长计算。
4. 独立的数据核查、定向调研、模型检查或图文工作可以并行；必要时可并行保留一条可交付路线与一个有明确下一项验证的探索分支，不强制两套完整实现。依赖同一结果的阶段等待真实输出，避免重复或互相覆盖。
5. 根据剩余时间、全题缺口和结构探索的预期价值分配工作。有低成本辨别检查时可以先探索；若检验没有带来新依据且交付开始受影响，则保留可用路线或收窄目标。不把算法升级当作创新，也不因路线非常规而要求先另做常规全题解。
6. 新发现和失败都可触发返回：观察提示更好表示时重新分析/探索，约束不满足回到建模/求解，数值不稳定先修数值；仅语句不清就在写作阶段修，不重跑无关计算。试探未成为主线时，保留有用认识和仍有效的成果。

## 交付与完成
长任务可维护 outputs/workflow/00-status.md，简记“阶段、实际成果路径、依据、未决问题、下一动作”；也可复用项目既有 task_plan/findings/progress，不建重复账本。区分已完成、部分完成、待输入和不适用。

给出本次已实现成果，而非仅调用计划。确认每个用户要求的交付物可定位，结果变更已传到受影响的图表和文字。所有历史练习放独立目录并标注年份，不计入当前比赛成果。
