# ---- Base image ----
FROM python:3.12-slim

# ---- System deps ----
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential python3-dev \
 && rm -rf /var/lib/apt/lists/*

# ---- Workdir ----
WORKDIR /app

# ---- Copy requirements first (CACHE QUAN TRỌNG) ----
COPY requirements.txt .

# ---- Install deps ----
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# ---- Copy source code ----
COPY . .

# ---- Expose ----
EXPOSE 8000

# ---- Run app (dev) ----
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
