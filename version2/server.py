from concurrent import futures
import datetime
import grpc
import editor_pb2
import editor_pb2_grpc
from pymongo import MongoClient
import json
from apscheduler.schedulers.background import BackgroundScheduler

# Establish a connection to the MongoDB server
client = MongoClient('mongodb://localhost:27017/')

# Select the MongoDB database
db = client['editor_db']

# Select collection in db
snapshots = db['snapshots']  


class EditorService(editor_pb2_grpc.EditorServiceServicer):
    def __init__(self):
        # Initialize the document state with a piece table structure
        self.originalBuffer = "Initial text of the document."
        self.addBuffer = ""
        self.pieces = [{"buffer": "original", "start": 0, "length": len(self.originalBuffer)}]

    def InsertText(self, request, context):
        # Logic to insert text into the addBuffer and update the piece table
        self.addBuffer += request.text
        new_piece = {"buffer": "add", "start": len(self.addBuffer) - len(request.text), "length": len(request.text)}
        self.pieces.append(new_piece)  # Simplified: appending to the end for illustration
        return editor_pb2.EditResponse(success=True)

    def DeleteText(self, request, context):
        return editor_pb2.EditResponse(success=True)

    def FetchDocument(self, request, context):
        # Reconstruct the document from the piece table for the response
        document = ""
        for piece in self.pieces:
            buffer = self.originalBuffer if piece["buffer"] == "original" else self.addBuffer
            start = piece["start"]
            length = piece["length"]
            document += buffer[start:start + length]
        return editor_pb2.FetchResponse(text=document)

    def FetchSerializedState(self, request, context):
        # Return the serialized state of the document (piece table)
        pieces = [editor_pb2.Piece(buffer=piece["buffer"], start=piece["start"], length=piece["length"]) for piece in self.pieces]
        return editor_pb2.SerializedDocumentState(originalBuffer=self.originalBuffer, addBuffer=self.addBuffer, pieces=pieces)


    def save_snapshot(self):
        # Serialize the current state
        snapshot = {
            "originalBuffer": self.originalBuffer,
            "addBuffer": self.addBuffer,
            "pieces": self.pieces,
            "timestamp": datetime.datetime.utcnow()  # Add a timestamp for the snapshot
        }

        # Save to MongoDB
        snapshots.insert_one(snapshot)

scheduler = BackgroundScheduler()
editorService = EditorService() # Create an instance of the class
scheduler.add_job(editorService.save_snapshot, 'interval', minutes=1) # Use the method from the instance
scheduler.start()

def serve():
    global editor_service_instance
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    editor_pb2_grpc.add_EditorServiceServicer_to_server(EditorService(), server)
    server.add_insecure_port('[::]:50051')
    print("Server started, listening on port 50051.")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()