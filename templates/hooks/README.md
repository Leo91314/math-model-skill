# 可选hooks

沿用原项目的两个轻量功能：SessionStart提示解释器与工作入口；Stop只做Python语法检查，输出摘要，不执行模型。

在仓库根目录生成指定项目的配置：

```bash
python3 scripts/configure_hooks.py --project /path/to/your-project
```

脚本自动填写实际路径，已有hooks会保留并停止覆盖。生成配置后，在Codex的 `/hooks` 中审阅具体定义；不会改写信任记录或全局配置。运行方式及信任要求见 [官方hooks文档](https://learn.chatgpt.com/docs/hooks)。
