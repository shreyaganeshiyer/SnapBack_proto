"""Create harmless, realistic-looking files in the simulated drive only."""
from __future__ import annotations

import csv
import shutil
from pathlib import Path

from docx import Document
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen.canvas import Canvas

import config
from core.events import emit

DEPARTMENTS = ("finance", "hr", "projects", "notes")
FILE_TYPES = ("txt", "csv", "docx", "xlsx", "pdf")


def _write_text(path: Path, number: int, department: str) -> None:
    path.write_text(
        f"{department.title()} operating notes {number}\n\n"
        "This is synthetic SnapBack demonstration content.\n"
        "It contains no real company or personal information.\n",
        encoding="utf-8",
    )


def _write_csv(path: Path, number: int, department: str) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["Record", "Department", "Status", "Amount"])
        writer.writerows([
            [f"SB-{number:03}-A", department.title(), "Approved", 1200],
            [f"SB-{number:03}-B", department.title(), "Review", 850],
        ])


def _write_docx(path: Path, number: int, department: str) -> None:
    document = Document()
    document.add_heading(f"{department.title()} Project Update {number}", 0)
    document.add_paragraph("Synthetic SnapBack demonstration document.")
    document.add_heading("Summary", level=1)
    document.add_paragraph(
        "This file is generated solely for the local ransomware recovery demo. "
        "It contains no real company or personal information."
    )
    document.save(path)


def _write_xlsx(path: Path, number: int, department: str) -> None:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Summary"
    sheet.append(["Record", "Department", "Status", "Value"])
    sheet.append([f"SB-{number:03}-A", department.title(), "Approved", 1200])
    sheet.append([f"SB-{number:03}-B", department.title(), "Review", 850])
    for cell in sheet[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="1F4E78")
    sheet.freeze_panes = "A2"
    for column, width in {"A": 16, "B": 18, "C": 14, "D": 12}.items():
        sheet.column_dimensions[column].width = width
    workbook.save(path)


def _write_pdf(path: Path, number: int, department: str) -> None:
    canvas = Canvas(str(path), pagesize=letter)
    canvas.setTitle(f"{department.title()} Brief {number}")
    canvas.setFont("Helvetica-Bold", 18)
    canvas.drawString(72, 720, f"{department.title()} Brief {number}")
    canvas.setFont("Helvetica", 11)
    canvas.drawString(72, 685, "Synthetic SnapBack demonstration document")
    canvas.drawString(72, 660, "This file contains no real company or personal information.")
    canvas.save()


WRITERS = {
    "txt": _write_text, "csv": _write_csv, "docx": _write_docx,
    "xlsx": _write_xlsx, "pdf": _write_pdf,
}


def generate_files() -> list[str]:
    """Reset and populate only the isolated simulated shared drive."""
    if config.SHARED_DIR.exists():
        shutil.rmtree(config.SHARED_DIR)
    
    files: list[str] = []

    for index in range(config.NUM_FILES):
        department = DEPARTMENTS[index % len(DEPARTMENTS)]
        extension = FILE_TYPES[index % len(FILE_TYPES)]
        folder = config.SHARED_DIR / department
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / f"{department}_record_{index + 1:02}.{extension}"
        WRITERS[extension](path, index + 1, department)
        files.append(path.relative_to(config.SHARED_DIR).as_posix())
    emit("setup_complete", files=len(files), file_types=list(FILE_TYPES))
    return files


if __name__ == "__main__":
    created = generate_files()
    print(f"Created {len(created)} synthetic files in {config.SHARED_DIR}")
