#export CORS_ALLOW_ORIGIN="http://localhost:5173"
export PYTHONPATH=$PYTHONPATH:/home/ubuntu/squadrun-open-webui/backend
PORT="${PORT:-8080}"
uvicorn open_webui.main:app --port $PORT --host 0.0.0.0 --forwarded-allow-ips '*'
