import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

STATIONS = [
    {
        "id": "kol-hai",
        "name": "קול חי",
        "url": "https://live.kcm.fm/live-new",
    },
    {
        "id": "kol-barama",
        "name": "קול ברמה",
        "url": "https://cdn.cybercdn.live/Kol_Barama/Live_Audio/icecast.audio",
    },
    {
        "id": "kol-hai-music",
        "name": "קול חי מיוזיק",
        "url": "https://live.kcm.fm/livemusic",
    },
    {
        "id": "kol-play",
        "name": "קול פליי",
        "url": "https://cdn.cybercdn.live/Kol_Barama/Music/icecast.audio",
    },
]

BASE_DIR = Path("recordings")


def record_station(station):
    station_dir = BASE_DIR / station["id"]
    station_dir.mkdir(parents=True, exist_ok=True)

    output_pattern = str(
        station_dir / "%Y-%m-%d_%H-00.mp3"
    )

    command = [
        "ffmpeg",

        # שקט יותר בלוגים
        "-hide_banner",
        "-loglevel", "warning",
        "-nostdin",

        # ניסיון התחברות מחדש אם הסטרים נופל
        "-reconnect", "1",
        "-reconnect_streamed", "1",
        "-reconnect_on_network_error", "1",
        "-reconnect_delay_max", "10",

        # מקור
        "-i", station["url"],

        # הקלטה רציפה
        "-vn",

        # MP3 קטן
        "-c:a", "libmp3lame",
        "-b:a", "32k",
        "-ar", "44100",
        "-ac", "2",

        # חיתוך לפי זמן מערכת
        "-f", "segment",
        "-segment_time", "3600",
        "-segment_atclocktime", "1",
        "-strftime", "1",

        # שמירת כל קובץ לפי שעת ההתחלה
        output_pattern,
    ]

    print(f"Starting recorder: {station['name']}")

    while True:
        process = subprocess.run(command)

        print(
            f"{station['name']} stopped "
            f"with exit code {process.returncode}. Restarting..."
        )


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(record_station, STATIONS)
