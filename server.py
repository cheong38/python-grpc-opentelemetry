import grpc
from concurrent import futures
import proto.hello_pb2
import proto.hello_pb2_grpc

class GreeterServicer(proto.hello_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        return proto.hello_pb2.HelloReply(message=f"Hello, {request.name}!")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    proto.hello_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("Server starting on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()