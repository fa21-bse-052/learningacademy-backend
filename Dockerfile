# 1. Base image
FROM python:3.11-slim

# 2. Prevent Python from buffering stdout/stderr (so logs show up immediately)
ENV PYTHONUNBUFFERED=1

# 3. Set working directory
WORKDIR /app

# 4. Install system dependencies (ffmpeg for MoviePy)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       ffmpeg \
       && rm -rf /var/lib/apt/lists/*

# 5. Copy & install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 6. Copy application code
COPY . .

# 7. Expose the port Uvicorn will run on
EXPOSE 8000

# 8. Default command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
