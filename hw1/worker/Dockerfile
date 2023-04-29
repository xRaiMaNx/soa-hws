FROM python:3.8-slim
ENV PIP_ROOT_USER_ACTION=ignore

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY ./utils/object.proto ./utils/
RUN python -m pip install --no-cache-dir grpcio-tools
RUN python -m grpc_tools.protoc -I=./utils --python_out=./utils object.proto
COPY . .

CMD ["python", "-m", "worker"]