import json
import os
import subprocess
import time
from datetime import datetime, timedelta, timezone


# ---------------------------------------------------------
# הגדרות
# ---------------------------------------------------------

STATIONS_FILE = "stations.json"
RECORDINGS_DIR = "recordings"
RETENTION_DAYS = 7

# אזור הזמן של ישראל
TIMEZONE = timezone(timedelta(hours=3))


# ---------------------------------------------------------
# טעינת התחנות
# ---------------------------------------------------------

def load_stations():
    with open(STATIONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------
# יצירת תיקיות
# ---------------------------------------------------------

def ensure_directories():
    os.makedirs(RECORDINGS_DIR, exist_ok=True)

    stations = load_stations()

    for station_id in stations:
        os.makedirs(
            os.path.join(RECORDINGS_DIR, station_id),
            exist_ok=True
        )


# ---------------------------------------------------------
# מחיקת הקלטות ישנות
# ---------------------------------------------------------

def delete_old_recordings():
    cutoff = datetime.now(TIMEZONE) - timedelta(days=RETENTION_DAYS)

    for station_id in load_stations():
        station_dir = os.path.join(RECORDINGS_DIR, station_id)

        if not os.path.exists(station_dir):
            continue

        for filename in os.listdir(station_dir):

            if not filename.endswith(".mp3"):
                continue

            filepath = os.path.join(station_dir, filename)

            try:
                modified_time = datetime.fromtimestamp(
                    os.path.getmtime(filepath),
                    tz=TIMEZONE
                )

                if modified_time < cutoff:
                    print(f"Deleting old recording: {filepath}")
                    os.remove(filepath)

            except Exception as e:
                print(f"Could not delete {filepath}: {e}")


# ---------------------------------------------------------
# הקלטת תחנה
# ---------------------------------------------------------

def record_station(station_id, station):

    station_name = station["name"]
    stream_url = station["stream"]

    while True:

        now = datetime.now(TIMEZONE)

        # תחילת השעה הנוכחית
        hour_start = now.replace(
            minute=0,
            second=0,
            microsecond=0
        )

        # סוף השעה
        hour_end = hour_start + timedelta(hours=1)

        filename = (
            hour_start.strftime("%Y-%m-%d_%H-00")
            + ".mp3"
        )

        station_dir = os.path.join(
            RECORDINGS_DIR,
            station_id
        )

        filepath = os.path.join(
            station_dir,
            filename
        )

        # כמה שניות נשארו עד סוף השעה
        remaining_seconds = (
            hour_end - now
        ).total_seconds()

        # לא להקליט מעבר לסוף השעה
        duration = max(1, int(remaining_seconds))

        print()
        print("=" * 60)
        print(f"Station: {station_name}")
        print(f"Stream: {stream_url}")
        print(f"File: {filepath}")
        print(f"Duration: {duration} seconds")
        print("=" * 60)

        command = [
            "ffmpeg",

            "-y",

            "-hide_banner",

            "-loglevel",
            "warning",

            "-i",
            stream_url,

            "-t",
            str(duration),

            "-vn",

            "-c:a",
            "libmp3lame",

            "-b:a",
            "128k",

            filepath
        ]

        try:

            result = subprocess.run(
                command,
                timeout=duration + 120
            )

            if result.returncode != 0:
                print(
                    f"FFmpeg exited with code "
                    f"{result.returncode}"
                )

        except subprocess.TimeoutExpired:

            print(
                f"FFmpeg timed out for "
                f"{station_name}"
            )

        except Exception as e:

            print(
                f"Recording error for "
                f"{station_name}: {e}"
            )

        # המתנה קצרה לפני ניסיון נוסף
        time.sleep(5)


# ---------------------------------------------------------
# הפעלת המערכת
# ---------------------------------------------------------

def main():

    print("Radio Recorder starting...")

    ensure_directories()

    stations = load_stations()

    print(
        f"Loaded {len(stations)} radio stations."
    )

    delete_old_recordings()

    # כרגע מפעילים כל תחנה בנפרד.
    # בהמשך נהפוך את זה להרצה מקבילית
    # כדי שכל ארבע התחנות יוקלטו בו-זמנית.

    for station_id, station in stations.items():

        print(
            f"Preparing station: "
            f"{station['name']}"
        )

        # כרגע רק בדיקה שהנתונים תקינים
        print(
            f"  ID: {station_id}"
        )

        print(
            f"  Stream: {station['stream']}"
        )


if __name__ == "__main__":
    main()
