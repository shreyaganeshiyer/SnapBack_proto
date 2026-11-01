from pathlib import Path

ROOT = Path(__file__).resolve().parent

STORAGE_DIR = ROOT / "storage"
SHARED_DIR = STORAGE_DIR / "shared_drive"
SNAPSHOT_DIR = STORAGE_DIR / "snapshots"

NUM_FILES = 60