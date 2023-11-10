#!/bin/bash
export http_proxy="http://host.docker.internal:7890"
export https_proxy="http://host.docker.internal:7890"
gunicorn -w ${WORKERS:=2} \
  -b :8000 -t ${TIMEOUT:=300} \
  -k uvicorn.workers.UvicornWorker \
  server:app