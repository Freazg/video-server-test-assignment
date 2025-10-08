FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir grpcio==1.75.1 grpcio-tools==1.75.1 aiortc pycryptodome av
COPY server/signaling.proto .
COPY server/server.py .
COPY server/sample.mp4.enc .
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. signaling.proto

CMD ["python", "server.py"]