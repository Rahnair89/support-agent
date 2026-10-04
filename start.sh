#!/bin/sh
for i in $(seq 1 30); do
 python src/rag/ingest.py && break
 echo "ingest attempt $i failed (Qdrant not ready?), retrying in 2s"
 sleep 2
done
exec uvicorn app.main:app --host 0.0.0.0 --port 8000