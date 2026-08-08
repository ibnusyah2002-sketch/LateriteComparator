from __future__ import annotations

import json
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
EXCEL_PATH = REPO_ROOT / "database" / "QAQC.xlsx"
DATASET_DIR = REPO_ROOT / "dataset"
OUTPUT_DIR = REPO_ROOT / "backend" / "data_preview"

SCAN_REQUIRED_COLUMNS = [
    "Code",
    "Ni",
    "Co",
    "Fe",
    "SiO2",
    "MgO",
    "Warna",
    "Zona",
    "Ukuran",
    "Komposisi",
    "Keterangan",
]

EXPECTED_COLUMNS = [
    "NO",
    "Code",
    "Tanggal Sample",
    "Kode Sample",
    "INCR",
    "Ni",
    "Co",
    "Fe",
    "SiO2",
    "CaO",
    "MgO",
    "Cr2O3",
    "AL2O3",
    "Cr",
    "Fe/Ni",
    "S/M",
    "BC",
    "Warna",
    "Zona",
    "Ukuran",
    "Komposisi",
    "Keterangan",
    "Dokumentasi (RAW)",
    "Dokumentasi (SI GC)",
    "PPT",
    "Front",
]

SAMPLE_FIELD_MAP = {
    "NO": "source_no",
    "Code": "code",
    "Tanggal Sample": "sample_date",
    "Kode Sample": "sample_code",
    "INCR": "incr",
    "Ni": "ni",
    "Co": "co",
    "Fe": "fe",
    "SiO2": "sio2",
    "CaO": "cao",
    "MgO": "mgo",
    "Cr2O3": "cr2o3",
    "AL2O3": "al2o3",
    "Cr": "cr",
    "Fe/Ni": "fe_ni",
    "S/M": "s_m",
    "BC": "bc",
    "Warna": "color",
    "Zona": "zone",
    "Ukuran": "size_text",
    "Komposisi": "composition",
    "Keterangan": "description",
    "Dokumentasi (RAW)": "documentation_raw",
    "Dokumentasi (SI GC)": "documentation_si_gc",
    "PPT": "ppt_reference",
    "Front": "front_reference",
}

IMAGE_RULES: list[dict[str, Any]] = [
    {
        "image_type": "raw",
        "accepted_filenames": [
            "raw.jpg",
            "raw.jpeg",
            "raw.png",
            "raw.webp",
        ],
        "required": True,
        "is_primary": True,
    },
    {
        "image_type": "scale",
        "accepted_filenames": [
            "scale.jpg",
            "scale.jpeg",
            "scale.png",
            "scale.webp",
            "scala.jpg",
            "scala.jpeg",
            "scala.png",
            "skala.jpg",
            "skala.jpeg",
            "skala.png",
        ],
        "required": False,
        "is_primary": False,
    },
]

XML_NS = {
    "main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "rel": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "pkgrel": "http://schemas.openxmlformats.org/package/2006/relationships",
}


def main() -> int:
    print("LCGC Database Asset Validation")
    print("=" * 36)

    validate_base_paths()

    rows = read_first_sheet(EXCEL_PATH)
    header_index, headers, data_rows = extract_table(rows)

    report = validate_assets(headers=headers, data_rows=data_rows)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    write_json(OUTPUT_DIR / "validation_report.json", report["validation_report"])
    write_json(
        OUTPUT_DIR / "comparator_samples_preview.json",
        report["comparator_samples_preview"],
    )
    write_json(
        OUTPUT_DIR / "comparator_images_preview.json",
        report["comparator_images_preview"],
    )

    print_summary(report["validation_report"], header_index)

    has_critical_issue = bool(
        report["validation_report"]["columns"]["missing_required_columns"]
        or report["validation_report"]["samples"]["empty_code_rows"]
        or report["validation_report"]["samples"]["duplicate_codes"]
        or report["validation_report"]["images"]["missing_folders"]
        or report["validation_report"]["images"]["missing_raw_images"]
    )

    if has_critical_issue:
        print("\nStatus: REVIEW REQUIRED")
        print("Some critical items need correction before Supabase import.")
        return 1

    print("\nStatus: PASS")
    print("Excel and image folders are ready for import preparation.")
    return 0


def validate_base_paths() -> None:
    if not EXCEL_PATH.exists():
        raise FileNotFoundError(f"Excel file not found: {to_repo_path(EXCEL_PATH)}")

    if not DATASET_DIR.exists():
        raise FileNotFoundError(f"Dataset folder not found: {to_repo_path(DATASET_DIR)}")


def read_first_sheet(xlsx_path: Path) -> list[list[str]]:
    with zipfile.ZipFile(xlsx_path) as workbook_zip:
        shared_strings = read_shared_strings(workbook_zip)
        sheet_path = get_first_sheet_path(workbook_zip)
        return read_worksheet_rows(workbook_zip, sheet_path, shared_strings)


def read_shared_strings(workbook_zip: zipfile.ZipFile) -> list[str]:
    shared_strings_path = "xl/sharedStrings.xml"

    if shared_strings_path not in workbook_zip.namelist():
        return []

    root = ET.fromstring(workbook_zip.read(shared_strings_path))
    strings: list[str] = []

    for string_item in root.findall("main:si", XML_NS):
        text_nodes = string_item.findall(".//main:t", XML_NS)
        strings.append("".join(node.text or "" for node in text_nodes))

    return strings


def get_first_sheet_path(workbook_zip: zipfile.ZipFile) -> str:
    workbook_root = ET.fromstring(workbook_zip.read("xl/workbook.xml"))
    relations_root = ET.fromstring(workbook_zip.read("xl/_rels/workbook.xml.rels"))

    first_sheet = workbook_root.find("main:sheets/main:sheet", XML_NS)

    if first_sheet is None:
        raise ValueError("No worksheet found in Excel file.")

    relation_id = first_sheet.attrib.get(f"{{{XML_NS['rel']}}}id")

    if not relation_id:
        raise ValueError("First worksheet relation ID not found.")

    for relation in relations_root.findall("pkgrel:Relationship", XML_NS):
        if relation.attrib.get("Id") == relation_id:
            target = relation.attrib["Target"].lstrip("/")
            if target.startswith("xl/"):
                return target
            return f"xl/{target}"

    raise ValueError("First worksheet path not found.")


def read_worksheet_rows(
    workbook_zip: zipfile.ZipFile,
    sheet_path: str,
    shared_strings: list[str],
) -> list[list[str]]:
    root = ET.fromstring(workbook_zip.read(sheet_path))
    parsed_rows: list[list[str]] = []

    for row_node in root.findall(".//main:sheetData/main:row", XML_NS):
        row_values: dict[int, str] = {}

        for cell in row_node.findall("main:c", XML_NS):
            cell_reference = cell.attrib.get("r", "")
            column_index = column_index_from_cell_reference(cell_reference)
            row_values[column_index] = read_cell_value(cell, shared_strings)

        if row_values:
            max_index = max(row_values.keys())
            parsed_rows.append(
                [row_values.get(index, "") for index in range(max_index + 1)]
            )

    return parsed_rows


def read_cell_value(cell: ET.Element, shared_strings: list[str]) -> str:
    cell_type = cell.attrib.get("t")

    if cell_type == "inlineStr":
        text_nodes = cell.findall(".//main:t", XML_NS)
        return clean_value("".join(node.text or "" for node in text_nodes))

    value_node = cell.find("main:v", XML_NS)

    if value_node is None or value_node.text is None:
        return ""

    raw_value = value_node.text

    if cell_type == "s":
        try:
            return clean_value(shared_strings[int(raw_value)])
        except (ValueError, IndexError):
            return ""

    return clean_value(raw_value)


def column_index_from_cell_reference(cell_reference: str) -> int:
    letters = "".join(char for char in cell_reference if char.isalpha()).upper()

    if not letters:
        return 0

    column_index = 0

    for char in letters:
        column_index = column_index * 26 + (ord(char) - ord("A") + 1)

    return column_index - 1


def extract_table(rows: list[list[str]]) -> tuple[int, list[str], list[dict[str, str]]]:
    header_index = find_header_row(rows)
    headers = [clean_value(value) for value in rows[header_index]]

    data_rows: list[dict[str, str]] = []

    for excel_row_number, row in enumerate(
        rows[header_index + 1 :],
        start=header_index + 2,
    ):
        row_dict: dict[str, str] = {"_excel_row_number": str(excel_row_number)}

        for index, header in enumerate(headers):
            if not header:
                continue

            row_dict[header] = clean_value(row[index]) if index < len(row) else ""

        if has_any_data(row_dict):
            data_rows.append(row_dict)

    return header_index, headers, data_rows


def find_header_row(rows: list[list[str]]) -> int:
    for index, row in enumerate(rows[:20]):
        normalized_values = {clean_value(value) for value in row}

        if "Code" in normalized_values:
            return index

    raise ValueError("Header row not found. Column 'Code' was not detected.")


def has_any_data(row_dict: dict[str, str]) -> bool:
    for key, value in row_dict.items():
        if key == "_excel_row_number":
            continue

        if clean_value(value):
            return True

    return False


def validate_assets(headers: list[str], data_rows: list[dict[str, str]]) -> dict[str, Any]:
    missing_expected_columns = [
        column for column in EXPECTED_COLUMNS if column not in headers
    ]
    missing_required_columns = [
        column for column in SCAN_REQUIRED_COLUMNS if column not in headers
    ]

    samples_preview: list[dict[str, Any]] = []
    images_preview: list[dict[str, Any]] = []

    empty_code_rows: list[int] = []
    duplicate_codes: dict[str, list[int]] = {}
    seen_codes: dict[str, list[int]] = {}

    missing_folders: list[dict[str, Any]] = []
    missing_raw_images: list[dict[str, Any]] = []
    missing_scale_images: list[dict[str, Any]] = []
    extra_files: list[dict[str, Any]] = []

    expected_file_names = {
        filename.lower()
        for rule in IMAGE_RULES
        for filename in rule["accepted_filenames"]
    }

    for row in data_rows:
        excel_row_number = int(row["_excel_row_number"])
        code = clean_code(row.get("Code", ""))

        if not code:
            empty_code_rows.append(excel_row_number)
            continue

        seen_codes.setdefault(code, []).append(excel_row_number)

        samples_preview.append(build_sample_preview(row, code))

        sample_folder = DATASET_DIR / code

        if not sample_folder.exists() or not sample_folder.is_dir():
            missing_folders.append(
                {
                    "excel_row_number": excel_row_number,
                    "code": code,
                    "expected_folder": to_repo_path(sample_folder),
                }
            )
            continue

        folder_files = [item for item in sample_folder.iterdir() if item.is_file()]

        for item in folder_files:
            if item.name.lower() not in expected_file_names:
                extra_files.append(
                    {
                        "code": code,
                        "file": to_repo_path(item),
                    }
                )

        for rule in IMAGE_RULES:
            image_path = find_first_existing_file_case_insensitive(
                sample_folder,
                rule["accepted_filenames"],
            )

            if image_path is None:
                issue = {
                    "excel_row_number": excel_row_number,
                    "code": code,
                    "expected_files": [
                        to_repo_path(sample_folder / filename)
                        for filename in rule["accepted_filenames"]
                    ],
                }

                if rule["image_type"] == "raw":
                    missing_raw_images.append(issue)
                elif rule["image_type"] == "scale":
                    missing_scale_images.append(issue)

                continue

            images_preview.append(
                {
                    "code": code,
                    "image_type": rule["image_type"],
                    "local_path": to_repo_path(image_path),
                    "storage_path": build_storage_path(
                        code,
                        rule["image_type"],
                        image_path,
                    ),
                    "is_primary": rule["is_primary"],
                }
            )

    for code, rows in seen_codes.items():
        if len(rows) > 1:
            duplicate_codes[code] = rows

    validation_report = {
        "source": {
            "excel_path": to_repo_path(EXCEL_PATH),
            "dataset_dir": to_repo_path(DATASET_DIR),
        },
        "columns": {
            "detected_columns": headers,
            "missing_expected_columns": missing_expected_columns,
            "missing_required_columns": missing_required_columns,
        },
        "samples": {
            "total_data_rows": len(data_rows),
            "rows_with_code": len(samples_preview),
            "unique_codes": len(seen_codes),
            "empty_code_rows": empty_code_rows,
            "duplicate_codes": duplicate_codes,
        },
        "images": {
            "expected_folder_rule": "dataset/{Code}/",
            "expected_images": {
                "raw": IMAGE_RULES[0]["accepted_filenames"],
                "scale": IMAGE_RULES[1]["accepted_filenames"],
            },
            "missing_folders": missing_folders,
            "missing_raw_images": missing_raw_images,
            "missing_scale_images": missing_scale_images,
            "extra_files": extra_files,
            "image_rows_preview_count": len(images_preview),
        },
    }

    return {
        "validation_report": validation_report,
        "comparator_samples_preview": samples_preview,
        "comparator_images_preview": images_preview,
    }


def build_sample_preview(row: dict[str, str], code: str) -> dict[str, Any]:
    sample: dict[str, Any] = {}

    for excel_column, database_field in SAMPLE_FIELD_MAP.items():
        value = row.get(excel_column, "")

        if excel_column == "Code":
            sample[database_field] = code
        else:
            sample[database_field] = value

    return sample


def find_first_existing_file_case_insensitive(
    folder: Path,
    accepted_filenames: list[str],
) -> Path | None:
    accepted_names = {filename.lower() for filename in accepted_filenames}

    for filename in accepted_filenames:
        exact_path = folder / filename

        if exact_path.exists():
            return exact_path

    for item in folder.iterdir():
        if item.is_file() and item.name.lower() in accepted_names:
            return item

    return None


def build_storage_path(code: str, image_type: str, image_path: Path) -> str:
    normalized_code = normalize_code_for_storage(code)
    extension = image_path.suffix.lower() or ".jpg"
    return f"comparator-images/{normalized_code}/{image_type}{extension}"


def normalize_code_for_storage(code: str) -> str:
    normalized = code.strip().lower()
    normalized = re.sub(r"\s+", "-", normalized)
    normalized = re.sub(r"[^a-z0-9-]", "-", normalized)
    normalized = re.sub(r"-+", "-", normalized)
    return normalized.strip("-")


def clean_code(value: str) -> str:
    return clean_value(value)


def clean_value(value: Any) -> str:
    if value is None:
        return ""

    return str(value).replace("\u00a0", " ").strip()


def to_repo_path(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_json(path: Path, data: Any) -> None:
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def print_summary(report: dict[str, Any], header_index: int) -> None:
    print(f"Excel file: {report['source']['excel_path']}")
    print(f"Dataset dir: {report['source']['dataset_dir']}")
    print(f"Header row: {header_index + 1}")
    print("")
    print("Column validation:")
    print(f"- Missing required columns: {len(report['columns']['missing_required_columns'])}")
    print(f"- Missing expected columns: {len(report['columns']['missing_expected_columns'])}")
    print("")
    print("Sample validation:")
    print(f"- Total data rows: {report['samples']['total_data_rows']}")
    print(f"- Rows with Code: {report['samples']['rows_with_code']}")
    print(f"- Unique Codes: {report['samples']['unique_codes']}")
    print(f"- Empty Code rows: {len(report['samples']['empty_code_rows'])}")
    print(f"- Duplicate Codes: {len(report['samples']['duplicate_codes'])}")
    print("")
    print("Image validation:")
    print(f"- Missing folders: {len(report['images']['missing_folders'])}")
    print(f"- Missing raw image: {len(report['images']['missing_raw_images'])}")
    print(f"- Missing scale image: {len(report['images']['missing_scale_images'])}")
    print(f"- Extra files: {len(report['images']['extra_files'])}")
    print(f"- Image rows preview: {report['images']['image_rows_preview_count']}")
    print("")
    print("Generated local reports:")
    print(f"- {to_repo_path(OUTPUT_DIR / 'validation_report.json')}")
    print(f"- {to_repo_path(OUTPUT_DIR / 'comparator_samples_preview.json')}")
    print(f"- {to_repo_path(OUTPUT_DIR / 'comparator_images_preview.json')}")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"\nValidation failed: {error}", file=sys.stderr)
        raise SystemExit(1)