FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONPATH=/app/src MODEL_CACHE=/app/models
COPY scripts/download_models.py scripts/
# Bake models into the image; the private task can't download them at runtime
RUN python scripts/download_models.py
COPY src/ ./src
COPY prompts/ ./prompts
COPY kb/ ./kb
COPY config/ ./config
COPY start.sh .
EXPOSE 8000
CMD ["./start.sh"]