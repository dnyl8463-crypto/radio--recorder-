import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path("recordings")

STATIONS = {
    "kol-hai": "קול חי",
    "kol-barama": "קול ברמה",
    "kol-hai-music": "קול חי מיוזיק",
    "kol-play": "קול פליי",
}

manifest = {
    "updated_at": datetime.now().isoformat(),
    "stations": []
}

for station_id, station_name in STATIONS.items():

    station = {
        "id": station_id,
        "name": station_name,
        "recordings": []
    }

    directory = BASE_DIR / station_id

    if directory.exists():

        for file in sorted(
            directory.rglob("*.mp3"),
            reverse=True
        ):

            # recordings/kol-hai/2026-08-10_21-00.mp3
            relative = file.relative_to(BASE_DIR)

            parts = file.stem.split("_")

            date = parts[0] if len(parts) > 0 else ""
            hour = parts[1].replace("-", ":") if len(parts) > 1 else ""

            station["recordings"].append({
                "date": date,
                "hour": hour,
                "path": str(relative)
            })

    manifest["stations"].append(station)


with open("recordings.json", "w", encoding="utf-8") as f:
    json.dump(
        manifest,
        f,
        ensure_ascii=False,
        indent=2
    )

print("recordings.json created successfully.")
