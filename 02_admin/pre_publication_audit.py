from pathlib import Path
from zipfile import ZipFile
import csv
import json
import re
import sqlite3
import subprocess

ROOT = Path(__file__).resolve().parents[1]

PATTERNS = {
    "Personal Windows path": re.compile(
        r"C:\\Users\\", re.IGNORECASE
    ),
    "OneDrive reference": re.compile(
        r"OneDrive", re.IGNORECASE
    ),
    "Potential credential": re.compile(
        r"(password|passwd|pwd|api[_-]?key|secret|token)"
        r"\s*[:=]\s*['\"]?[^\s,'\";]{4,}",
        re.IGNORECASE
    ),
    "Private key": re.compile(
        r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
    ),
}

findings = []
review_items = []
checked = {
    "documents": 0,
    "spreadsheets": 0,
    "csv": 0,
    "database_cells": 0,
    "notebooks": 0,
}


def scan_text(text, location):
    for label, pattern in PATTERNS.items():
        if pattern.search(text):
            findings.append(f"{location}: {label}")


def inspect_office_files():
    paths = list(ROOT.rglob("*.docx")) + list(ROOT.rglob("*.xlsx"))

    for path in paths:
        if ".venv" in path.parts:
            continue

        if path.suffix == ".docx":
            checked["documents"] += 1
        else:
            checked["spreadsheets"] += 1

        try:
            with ZipFile(path) as archive:
                for name in archive.namelist():
                    if name.endswith((".xml", ".rels")):
                        data = archive.read(name)
                        text = data.decode("utf-8", errors="replace")
                        scan_text(text, f"{path.name}/{name}")

                    if any(term in name.lower() for term in (
                        "connections",
                        "externallink",
                        "mashup",
                        "query",
                        "comments",
                    )):
                        review_items.append(
                            f"{path.name}: inspect {name}"
                        )

                    if name.endswith(".bin"):
                        review_items.append(
                            f"{path.name}: binary component {name}"
                        )

        except Exception as exc:
            findings.append(f"{path.name}: inspection error: {exc}")


def inspect_csv():
    for path in ROOT.rglob("*.csv"):
        if ".venv" in path.parts:
            continue

        checked["csv"] += 1

        try:
            with path.open(
                "r", encoding="utf-8-sig",
                errors="replace", newline=""
            ) as file:
                reader = csv.reader(file)

                for row_number, row in enumerate(reader, 1):
                    for value in row:
                        scan_text(
                            value,
                            f"{path.name}, row {row_number}"
                        )

        except Exception as exc:
            findings.append(f"{path.name}: inspection error: {exc}")


def inspect_sqlite():
    for path in ROOT.rglob("*.db"):
        if ".venv" in path.parts:
            continue

        try:
            uri = path.resolve().as_uri() + "?mode=ro"
            connection = sqlite3.connect(uri, uri=True)

            tables = connection.execute(
                "SELECT name FROM sqlite_master "
                "WHERE type='table'"
            ).fetchall()

            for (table,) in tables:
                safe_table = '"' + table.replace('"', '""') + '"'

                cursor = connection.execute(
                    f"SELECT * FROM {safe_table}"
                )

                for row_number, row in enumerate(cursor, 1):
                    for value in row:
                        if isinstance(value, str):
                            checked["database_cells"] += 1
                            scan_text(
                                value,
                                f"{path.name}/{table}, row {row_number}"
                            )

            connection.close()

        except Exception as exc:
            findings.append(f"{path.name}: inspection error: {exc}")


def inspect_notebooks():
    for path in ROOT.rglob("*.ipynb"):
        if ".venv" in path.parts:
            continue

        checked["notebooks"] += 1

        try:
            notebook = json.loads(
                path.read_text(encoding="utf-8")
            )

            if "cells" not in notebook:
                findings.append(
                    f"{path.name}: missing cells"
                )

            scan_text(
                json.dumps(notebook, ensure_ascii=False),
                path.name
            )

        except Exception as exc:
            findings.append(
                f"{path.name}: invalid notebook: {exc}"
            )


def inspect_git():
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True
    )

    tracked = result.stdout.splitlines()

    for name in tracked:
        if any(part in name for part in (
            ".venv/",
            "__pycache__/",
            ".env",
            ".ipynb.bak",
        )):
            findings.append(f"Tracked unwanted file: {name}")

    return len(tracked)


def main():
    print("NOVA CORPORATION BR001")
    print("PRE-PUBLICATION AUDIT")
    print("=" * 55)

    inspect_office_files()
    inspect_csv()
    inspect_sqlite()
    inspect_notebooks()
    tracked_count = inspect_git()

    print("\nINSPECTION SUMMARY")
    print(f"Tracked Git files: {tracked_count}")

    for category, count in checked.items():
        print(f"{category}: {count}")

    print("\nAUTOMATED FINDINGS:", len(findings))

    for finding in findings[:50]:
        print("REVIEW:", finding)

    if len(findings) > 50:
        print("Additional findings omitted from display.")

    print("\nMANUAL REVIEW ITEMS:", len(review_items))

    for item in review_items[:30]:
        print("MANUAL REVIEW:", item)

    print("\nAUDIT FINISHED")
    print(
        "Automated checks do not certify that files are "
        "safe for public release."
    )


if __name__ == "__main__":
    main()
