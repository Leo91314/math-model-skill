# 中文数模LaTeX空白模板

沿用原项目实际使用的 `cumcm2026.sty` 与分章节入口，重新生成空白正文，不包含赛题答案、真实表格或论文图。

```bash
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
```

也可在Overleaf选择XeLaTeX，以main.tex为入口。默认Fandol字体，避免绑定原Mac字体。

样式内摘要一页、正文30页等提醒是2026原项目配置，不是所有比赛或年份的通用规定。AI声明和参考文献位置也应按当届正式要求调整。本模板由原项目本地排版形成，不宣称是官方模板。
