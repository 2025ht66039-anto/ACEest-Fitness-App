FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    python3-tk \
    tk \
    tcl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV DOCKER_ENV=true

CMD ["python", "app.py"]