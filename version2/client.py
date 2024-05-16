import grpc
import editor_pb2
import editor_pb2_grpc

def run():
    # Establish a channel with the server
    with grpc.insecure_channel('localhost:50051') as channel:
        # Create a stub (client)
        stub = editor_pb2_grpc.EditorServiceStub(channel)
        
        # Make an InsertText RPC call
        insert_response = stub.InsertText(editor_pb2.InsertRequest(position=0, text="Hello, world!"))
        print(f"InsertText response: {insert_response.success}")

        # Make a DeleteText RPC call
        delete_response = stub.DeleteText(editor_pb2.DeleteRequest(startPosition=0, endPosition=5))
        print(f"DeleteText response: {delete_response.success}")

        # Make a FetchDocument RPC call to get the current document state
        fetch_response = stub.FetchDocument(editor_pb2.FetchRequest())
        print(f"Current document state: {fetch_response.text}")

        # Make a FetchSerializedState RPC call to get the serialized state of the document
        fetch_serialized_response = stub.FetchSerializedState(editor_pb2.FetchRequest())
        print("Serialized document state:")
        print(f"Original Buffer: {fetch_serialized_response.originalBuffer}")
        print(f"Add Buffer: {fetch_serialized_response.addBuffer}")
        print("Pieces:")
        for piece in fetch_serialized_response.pieces:
            print(f"Buffer: {piece.buffer}, Start: {piece.start}, Length: {piece.length}")

if __name__ == '__main__':
    run()