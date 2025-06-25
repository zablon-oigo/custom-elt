FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y postgresql-client-16 && \
    rm -rf /var/lib/apt/lists/*

COPY main.py .

CMD ["python", "main.py"]
