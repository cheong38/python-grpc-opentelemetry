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

## 결과

클라이언트와 서버에서 각각 gRPC 서비스에 대해 instrumentation 을 수행한다.
그리고 클라이언트에서 서버로 요청을 전송할 때 metadata 에 tracing 정보를 추가하도록 하였다.

클라이언트에서 출력한 span 의 결과를 보면 아래와 같다.

```json
{
    "name": "Client Request",
    "context": {
        "trace_id": "0xe7ea3095e371e7d66c407bc6d2115279",
        "span_id": "0x4ab7949cd754c41f",
        "trace_state": "[]"
    },
    "kind": "SpanKind.INTERNAL",
    "parent_id": null,
    "start_time": "2024-10-02T09:05:05.608472Z",
    "end_time": "2024-10-02T09:05:05.611589Z",
    "status": {
        "status_code": "UNSET"
    },
    "attributes": {},
    "events": [],
    "links": [],
    "resource": {
        "attributes": {
            "telemetry.sdk.language": "python",
            "telemetry.sdk.name": "opentelemetry",
            "telemetry.sdk.version": "1.27.0",
            "service.name": "unknown_service"
        },
        "schema_url": ""
    }
}
```

이 클라이언트의 요청을 받은 서버에서 출력한 span 의 결과를 보면 아래와 같다.

```json
{
  "name": "/Greeter/SayHello",
  "context": {
    "trace_id": "0xe7ea3095e371e7d66c407bc6d2115279",
    "span_id": "0x960e1c479d66922e",
    "trace_state": "[]"
  },
  "kind": "SpanKind.SERVER",
  "parent_id": "0x4ab7949cd754c41f",
  "start_time": "2024-10-02T09:05:05.611218Z",
  "end_time": "2024-10-02T09:05:05.611296Z",
  "status": {
    "status_code": "UNSET"
  },
  "attributes": {
    "rpc.system": "grpc",
    "rpc.grpc.status_code": 0,
    "rpc.method": "SayHello",
    "rpc.service": "Greeter",
    "rpc.user_agent": "grpc-python/1.66.2 grpc-c/43.0.0 (osx; chttp2)",
    "net.peer.ip": "[::1]",
    "net.peer.port": "65504",
    "net.peer.name": "localhost"
  },
  "events": [],
  "links": [],
  "resource": {
    "attributes": {
      "telemetry.sdk.language": "python",
      "telemetry.sdk.name": "opentelemetry",
      "telemetry.sdk.version": "1.27.0",
      "service.name": "unknown_service"
    },
    "schema_url": ""
  }
}
```

서버에서 새로운 trace_id 를 생성하지 않고, 클라이언트에서 전송한 trace_id 를 사용하여 span 을 생성한 것을 확인할 수 있으며,
서버에서 출력한 span 에서 parent_id 가 null 이 아닌 클라이언트에서 보낸 span_id 를 사용하고 있음을 확인할 수 있다.
이로써 클라이언트와 서버 간의 tracing 이 잘 이루어지고 있음을 확인할 수 있다.
