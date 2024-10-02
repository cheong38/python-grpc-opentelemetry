import grpc
from concurrent import futures

from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.trace import get_current_span

import proto.hello_pb2
import proto.hello_pb2_grpc
from absl import app
import asyncio
from opentelemetry.instrumentation.grpc import GrpcAioInstrumentorServer
from opentelemetry import trace


class GreeterServicer(proto.hello_pb2_grpc.GreeterServicer):
    async def SayHello(self, request, context):
        span = get_current_span()
        print(span.get_span_context())
        return proto.hello_pb2.HelloReply(message=f"Hello, {request.name}!")

async def serve():
    GrpcAioInstrumentorServer().instrument()
    trace.set_tracer_provider(TracerProvider())
    trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    server = grpc.aio.server(migration_thread_pool=futures.ThreadPoolExecutor(max_workers=10))
    proto.hello_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("Server starting on port 50051...")
    await server.start()
    await server.wait_for_termination()

def main(_args):
    del _args # Unused.

    asyncio.run(serve())

if __name__ == '__main__':
    app.run(main)
