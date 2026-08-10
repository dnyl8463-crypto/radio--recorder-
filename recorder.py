import subprocess
from concurrent.futures import ThreadPoolExecutor

STATIONS = [
    {
        "id": "kol-hai",
        "name": "קול חי",
        "url": "https://live.kcm.fm/live-new"
    },
    {
        "id": "kol-barama",
        "name": "קול ברמה",
        "url": "https://cdn.cybercdn.live/Kol_Barama/Live_Audio/icecast.audio"
    },
    {
        "id": "kol-hai-music",
        "name": "קול חי מיוזיק",
        "url": "https://live.kcm.fm/livemusic"
    },
    {
        "id": "kol-play",
        "name": "קול פליי",
        "url": "https://cdn.cybercdn.live/Kol_Barama/Music/icecast.audio"
    }
]

def record(station):
    output = f"{station['id']}.mp3"

    command = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel", "warning",
        "-nostdin",

        "-reconnect", "1",
        "-reconnect_streamed", "1",
        "-reconnect_delay_max", "10",

        "-i", station["url"],

        "-t", "3600",

        "-vn",
        "-c:a", "libmp3lame",
        "-b:a", "32k",
        "-ar", "44100",
        "-ac", "2",

        "-y",
        output
    ]

    print(f"Starting: {station['name']}")

    result = subprocess.run(command)

    if result.returncode == 0:
        print(f"Finished: {station['name']}")
    else:
        print(f"ERROR: {station['name']}")

with ThreadPoolExecutor(max_workers=4) as executor:
    executor.map(record, STATIONS)
