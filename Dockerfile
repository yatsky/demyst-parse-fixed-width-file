# Use the official Python image as the base image
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

VOLUME ["/app/sample_files"]

# Run the main Python script
ENTRYPOINT ["python", "main.py"]
