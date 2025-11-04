import logging
from flask_socketio import SocketIO

socketio = SocketIO()

class SocketIOHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        socketio.emit('log', {'data': log_entry})

def setup_logging(app):
    # Configure logging
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Get the root logger
    logger = logging.getLogger()
    
    # Create a SocketIO handler and add it to the root logger
    socketio_handler = SocketIOHandler()
    socketio_handler.setLevel(logging.INFO)
    logger.addHandler(socketio_handler)
    
    # Initialize SocketIO with the Flask app
    socketio.init_app(app)