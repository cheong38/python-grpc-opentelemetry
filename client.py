import grpc
import proto.hello_pb2 as hello_pb2
import proto.hello_pb2_grpc as hello_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = hello_pb2_grpc.GreeterStub(channel)

        response = stub.SayHello(hello_pb2.HelloRequest(name='Woojin'))
        print(f"SayHello Response: {response.message}")

if __name__ == '__main__':
    run()
