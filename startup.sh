#!/bin/bash
export PORT=${PORT:-8000}
cd backend
gunicorn -w 2 -k uvicorn.workers.UvicornWorker main:app --bind=0.0.0.0:$PORT