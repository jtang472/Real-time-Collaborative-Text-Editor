from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

def broadcast_document_state(document_state):
    socketio.emit('document_update', {'text': document_state})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
