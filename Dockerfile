FROM python:3.11-slim

WORKDIR /app

# Install ffmpeg and minimal tools
#RUN apt-get update && apt-get install -y ffmpeg && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy source code
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Run the FastAPI app in background + start your bot
CMD uvicorn app:app --host 0.0.0.0 --port 8000 & python3 main.py
