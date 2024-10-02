# Python gRPC OpenTelemetry Example

python 에서 gRPC 서버를 사용할 때 OpenTelemetry를 이용하여 tracing을 하는 예제입니다.

## Pre-requisites

- Python 3.10

## 가상환경 설정 및 의존성 설치

```bash
python -m venv .venv/
source .venv/bin/activate
pip install -r requirements.txt
```

## Compile proto file

```bash
$ python -m grpc_tools.protoc \
  --proto_path ./ \
  --python_out ./ \
  --grpc_python_out ./ \
  proto/hello.proto
```

## Run server

```bash
$ python server.py
```

## Run Client

다른 터미널에서 실행한다.

```bash
$ python client.py
```
