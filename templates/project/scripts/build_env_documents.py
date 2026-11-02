"""Build one-page Chinese DOCX/LaTeX diagnostics using the Codex document runtime."""

import json
from html import escape
from pathlib import Path

from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Pt, RGBColor

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "env_check"
# The bundled headless LibreOffice needs explicit font discovery on this Mac.
# Use local TeX fonts as a render-only fallback; the DOCX keeps macOS Songti SC.
font_config = ROOT / ".cache" / "fontconfig.conf"
font_config.parent.mkdir(parents=True, exist_ok=True)
font_config.write_text(
    '<?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "fonts.dtd"><fontconfig>'
    '<dir>/System/Library/Fonts</dir><dir>/System/Library/Fonts/Supplemental</dir>'
    '<dir>/Library/Fonts</dir>'
    f'<dir>{escape(str(Path.home() / "Library/TinyTeX/texmf-dist/fonts/opentype/public/fandol"))}</dir>'
    f'<cachedir>{escape(str(ROOT / ".cache" / "fontconfig"))}</cachedir>'
    '<alias binding="strong"><family>Songti SC</family>'
    '<prefer><family>FandolSong</family></prefer></alias></fontconfig>',
    encoding="utf-8",
)
result = json.loads((OUT / "results.json").read_text())
metrics = [
    ("检查项目", "环境测试结果"),
    ("合成数据样本量", str(result["sample_count"])),
    ("拟合冷却系数", f'{result["fitted_k_per_min"]:.6f} / min'),
    ("拟合均方根误差", f'{result["fit_rmse_C"]:.6f} °C'),
    ("线性规划最大值", f'{result["linear_program_maximum"]:.1f}'),
]
doc = Document()
section = doc.sections[0]
section.page_width, section.page_height = Cm(21), Cm(29.7)
section.top_margin = section.bottom_margin = Cm(2.0)
section.left_margin = section.right_margin = Cm(2.2)
for name, size in [("Normal", 11), ("Title", 20), ("Heading 1", 13), ("Caption", 10)]:
    style = doc.styles[name]
    style.font.name = "Songti SC"
    style.element.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), "Songti SC")
    style.font.size = Pt(size)
    style.font.color.rgb = RGBColor(0, 0, 0)
    for attribute in ("asciiTheme", "eastAsiaTheme", "hAnsiTheme", "cstheme"):
        style.element.rPr.rFonts.attrib.pop(qn("w:" + attribute), None)
    for border in style.element.xpath(".//w:pBdr"):
        border.getparent().remove(border)
    style.paragraph_format.space_after = Pt(7)
    style.paragraph_format.line_spacing = 1.15
doc.add_paragraph("数学建模环境测试报告", style="Title")
doc.add_paragraph(
    "本报告仅用于确认本地数据处理、常微分方程拟合、约束优化和中文文档导出链路可用。"
    "所有数据均为固定随机种子生成的合成数据，不是赛题数据或竞赛研究结论。"
)
doc.add_paragraph("数值链路", style="Heading 1")
doc.add_paragraph("合成 CSV → 牛顿冷却方程数值积分 → 参数拟合 → HiGHS 约束优化 → 图表及文档。")
equation = doc.add_paragraph()
math = OxmlElement("m:oMath")
run = OxmlElement("m:r")
text = OxmlElement("m:t")
text.text = "dT/dt = −k(T − 20),  T(0) = 80"
run.append(text)
math.append(run)
equation._p.append(math)
table = doc.add_table(rows=0, cols=2)
table.autofit = False
table.columns[0].width, table.columns[1].width = Cm(7), Cm(9.6)
for row_i, row_values in enumerate(metrics):
    row = table.add_row()
    for cell, value in zip(row.cells, row_values):
        cell.text = value
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        props = cell._tc.get_or_add_tcPr()
        borders = OxmlElement("w:tcBorders")
        for edge in ("top", "left", "bottom", "right"):
            border = OxmlElement("w:" + edge)
            for key, val in (("val", "single"), ("sz", "4"), ("color", "D9D9D9")):
                border.set(qn("w:" + key), val)
            borders.append(border)
        props.append(borders)
        if row_i == 0:
            shading = OxmlElement("w:shd")
            shading.set(qn("w:fill"), "E9EFF3")
            props.append(shading)
            cell.paragraphs[0].runs[0].bold = True
        for p in cell.paragraphs:
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(4)
doc.add_paragraph("合成数据与拟合曲线", style="Heading 1")
doc.add_picture(str(OUT / "synthetic_cooling.png"), width=Inches(6.15))
doc.add_paragraph("随机种子 20260910。真实测试参数 k = 0.12 / min。", style="Caption")
doc.save(OUT / "environment_check.docx")

latex = r"""\documentclass[UTF8,fontset=fandol,11pt]{ctexart}
\usepackage[a4paper,margin=2.2cm]{geometry}
\usepackage{amsmath,graphicx,booktabs}
\setlength{\parindent}{0pt}
\setlength{\parskip}{0.6em}
\title{数学建模环境测试报告}
\author{}\date{}
\begin{document}
\maketitle\vspace{-3em}
本报告用于确认本地数据处理、常微分方程拟合、约束优化和中文文档导出链路可用。
\textbf{所有数据均为合成环境测试数据，不是赛题数据或竞赛研究结论。}
\section*{数值链路}
合成 CSV $\rightarrow$ 常微分方程数值积分 $\rightarrow$ 参数拟合
$\rightarrow$ HiGHS 约束优化 $\rightarrow$ 图表及文档。
\[
\frac{\mathrm{d}T}{\mathrm{d}t}=-k(T-20),\qquad T(0)=80.
\]
\begin{center}
\begin{tabular}{ll}\toprule
检查项目 & 环境测试结果\\\midrule
__ROWS__
\bottomrule\end{tabular}
\end{center}
\section*{合成数据与拟合曲线}
\begin{center}
\includegraphics[width=0.92\linewidth]{synthetic_cooling.png}
\end{center}
随机种子 20260910。真实测试参数 $k=0.12\,\mathrm{min}^{-1}$。
\end{document}
"""
rows = "\n".join(f"{name} & {value.replace('°C', r'$^\circ$C')}\\\\" for name, value in metrics[1:])
(OUT / "environment_check.tex").write_text(latex.replace("__ROWS__", rows), encoding="utf-8")
print("Generated Chinese DOCX and LaTeX diagnostic documents.")
