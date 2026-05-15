#!/usr/bin/env python3
"""
Clean a simple contacts CSV:
- trims whitespace from headers and cells
- lowercases email addresses
- normalizes common US phone formats to 555-123-4567
- removes duplicate rows by email when an email exists

Usage:
  python clean_csv.py messy_contacts.csv cleaned_contacts.csv
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path


def clean_header(value: str) -> str:
    return re.sub(r"\s+", "_", value.strip().lower())


def clean_phone(value: str) -> str:
    digits = re.sub(r"\D", "", value)
    if len(digits) == 10:
        return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
    return value.strip()


def clean_cell(header: str, value: str) -> str:
    cleaned = value.strip()
    if header in {"email", "email_address"}:
        return cleaned.lower()
    if header == "phone":
        return clean_phone(cleaned)
    return re.sub(r"\s+", " ", cleaned)


def clean_csv(input_path: Path, output_path: Path) -> int:
    with input_path.open("r", newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames is None:
            raise ValueError("Input CSV has no header row.")

        headers = [clean_header(header) for header in reader.fieldnames]
        rows: list[dict[str, str]] = []
        seen_emails: set[str] = set()

        for raw_row in reader:
            row = {
                clean_header(key): clean_cell(clean_header(key), value or "")
                for key, value in raw_row.items()
                if key is not None
            }
            email = row.get("email_address") or row.get("email")
            if email:
                if email in seen_emails:
                    continue
                seen_emails.add(email)
            rows.append(row)

    with output_path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    return len(rows)


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: python clean_csv.py input.csv output.csv", file=sys.stderr)
        return 2

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    count = clean_csv(input_path, output_path)
    print(f"Wrote {count} cleaned rows to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
