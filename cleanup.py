from pathlib import Path
from datetime import datetime, timedelta

BASE_DIR = Path("recordings")
MAX_AGE = timedelta(days=7)

now = datetime.now()

if not BASE_DIR.exists():
    print("No recordings directory.")
    raise SystemExit(0)

deleted = 0

for file in BASE_DIR.rglob("*.mp3"):

    try:
        modified = datetime.fromtimestamp(file.stat().st_mtime)

        if now - modified > MAX_AGE:
            print(f"Deleting: {file}")
            file.unlink()
            deleted += 1

    except FileNotFoundError:
        pass

print(f"Deleted {deleted} old recordings.")
