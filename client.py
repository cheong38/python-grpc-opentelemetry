import grpc
from opentelemetry.propagate import inject

import proto.hello_pb2 as hello_pb2
import proto.hello_pb2_grpc as hello_pb2_grpc
from opentelemetry.instrumentation.grpc import GrpcAioInstrumentorClient
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)


def run():
    trace.set_tracer_provider(TracerProvider())
    tracer = trace.get_tracer_provider().get_tracer(__name__)

    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(ConsoleSpanExporter())
    )

    GrpcAioInstrumentorClient().instrument()
    with grpc.insecure_channel('localhost:50051') as channel:
        with tracer.start_as_current_span("Client Request"):
            stub = hello_pb2_grpc.GreeterStub(channel)
            trace_info = {}
            inject(trace_info)
            # metadata 는 (key, value) 쌍의 리스트로 구성되어야 해서 dict 를 포맷에 맞게 변경
            metadata = list(trace_info.items())
            response = stub.SayHello(hello_pb2.HelloRequest(name='Woojin'), metadata=metadata)
            print(f"SayHello Response: {response.message}")

if __name__ == '__main__':
    run()
