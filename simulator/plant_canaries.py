from __future__ import annotations
import csv
import json
import config


CANARIES = {
    "finance/Q4_salaries.csv": [
        ["Employee ID", "Department", "Salary"],
        ["DEMO-001", "Finance", "75000"],
        ["DEMO-002", "HR", "68000"],
    ],
    "hr/passwords_backup.txt": (
        "SYNTHETIC SNAPBACK DECOY\n"
        "This is not a real password file.\n"
        "Any change to this file should raise a canary alert.\n"
    ),
    "bank_details.txt": (
        "SYNTHETIC SNAPBACK DECOY\n"
        "This file contains no banking information.\n"
        "Any change to this file should raise a canary alert.\n"
    ),
    "projects/executive_notes.txt": (
        "SYNTHETIC SNAPBACK DECOY\n"
        "Demo executive project notes.\n"
        "Any change to this file should raise a canary alert.\n"
    ),
}


def plant_canaries() -> list[str]:
    if not config.SHARED_DIR.exists():
        raise FileNotFoundError(
            "Shared drive does not exist. Run generate_files first."
        )

    planted_paths = []

    for relative_path, content in CANARIES.items():

        file_path = config.SHARED_DIR / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)

        if file_path.suffix == ".csv":
            with file_path.open("w", newline="", encoding="utf-8") as file:
                csv.writer(file).writerows(content)
        else:
            file_path.write_text(content, encoding="utf-8")

        planted_paths.append(relative_path)

    canary_manifest = config.STORAGE_DIR / "canaries.json" 
    # detector will read that file and instantly raise CANARY_HIT if any listed canary’s hash changes.

    canary_manifest.write_text(
        json.dumps(planted_paths, indent=2),
        encoding="utf-8",
    )

    return planted_paths


if __name__ == "__main__":
    planted = plant_canaries()
    print(f"Planted {len(planted)} synthetic canary files:")
    for path in planted:
        print(f" - {path}")