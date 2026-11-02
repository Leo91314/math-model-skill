"""Check document structure/text; rendered pages still require visual inspection."""

import json
from pathlib import Path

import pymupdf
from docx import Document
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "env_check"
document = Document(OUT / "environment_check.docx")
assert "环境测试" in document.paragraphs[0].text
assert len(document.tables) == 1 and len(document.inline_shapes) == 1
assert len(document._element.xpath(".//m:oMath")) == 1
pdf_pages = {}
for path in [OUT / "environment_check.pdf", OUT / "docx_render" / "environment_check.pdf"]:
    reader = PdfReader(path)
    assert len(reader.pages) == 1
    text = "".join(page.extract_text() for page in reader.pages)
    assert "合成" in text and "0.119952" in text
    with pymupdf.open(path) as pdf:
        assert "合成" in "".join(page.get_text() for page in pdf)
    pdf_pages[str(path.relative_to(ROOT))] = len(reader.pages)
assert (OUT / "pdf_preview.png").exists()
assert (OUT / "docx_render" / "page-1.png").exists()
report_path = OUT / "environment_report.json"
report = json.loads(report_path.read_text())
report["artifacts"] = {"structural_checks": "passed", "rendered_pages": pdf_pages}
report_path.write_text(json.dumps(report, indent=2) + "\n")
print("Chinese PDF, DOCX, native equation, embedded plot and rendered pages checked.")
