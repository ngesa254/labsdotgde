FROM python:3.11.14-slim
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
WORKDIR /app
COPY requirements.lock requirements.lock
RUN pip install --no-cache-dir -r requirements.lock
COPY . .
USER 65532:65532
CMD ["python", "server.py"]
