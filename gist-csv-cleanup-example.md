# Python CSV Cleanup Example

This is a safe public sample of a small CSV cleanup automation.

It demonstrates the kind of focused task I can do as a $20 Fiverr order:

- Trim messy headers and cells
- Lowercase email addresses
- Normalize common 10-digit US phone numbers
- Remove duplicate contacts by email
- Write a clean output CSV

Fiverr checkout for a focused Python script:
https://www.fiverr.com/epowell2/write-a-small-python-script-for-csv-or-file-cleanup

Fiverr checkout for CSV/Excel cleanup:
https://www.fiverr.com/epowell2/clean-format-and-organize-your-csv-or-excel-file

Full sample repo:
https://github.com/epowell40/quick-automation-help/tree/main/samples/csv_cleanup

```python
#!/usr/bin/env python3
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

    count = clean_csv(Path(sys.argv[1]), Path(sys.argv[2]))
    print(f"Wrote {count} cleaned rows to {sys.argv[2]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```
