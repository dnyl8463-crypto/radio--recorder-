FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY recorder.py .
COPY cleanup.py .

RUN mkdir -p /app/recordings

CMD ["python3", "recorder.py"]
