import argparse
import csv
from pathlib import Path


def load_manifest(path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {"current_name", "new_name"}
        if set(reader.fieldnames or []) < required:
            raise ValueError("Manifest must include current_name and new_name columns.")
        return list(reader)


def validate_name(name):
    candidate = Path(name)
    if candidate.name != name or name in {"", ".", ".."}:
        raise ValueError(f"Unsafe file name in manifest: {name!r}")


def plan_renames(rows, folder):
    planned = []
    for row in rows:
        current_name = (row.get("current_name") or "").strip()
        new_name = (row.get("new_name") or "").strip()
        validate_name(current_name)
        validate_name(new_name)

        source = folder / current_name
        target = folder / new_name
        planned.append((source, target))
    return planned


def run(planned, apply_changes):
    for source, target in planned:
        if not source.exists():
            print(f"SKIP missing: {source.name}")
            continue
        if target.exists():
            print(f"SKIP target exists: {target.name}")
            continue

        if apply_changes:
            source.rename(target)
            print(f"RENAMED {source.name} -> {target.name}")
        else:
            print(f"DRY RUN {source.name} -> {target.name}")


def main():
    parser = argparse.ArgumentParser(description="Rename files from a CSV manifest.")
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--folder", required=True, type=Path)
    parser.add_argument("--apply", action="store_true", help="Rename files instead of previewing.")
    args = parser.parse_args()

    rows = load_manifest(args.manifest)
    planned = plan_renames(rows, args.folder)
    run(planned, args.apply)


if __name__ == "__main__":
    main()
