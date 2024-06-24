import socket
from message_formats import sensor_vals_pb2
from message_formats import commands_pb2
import msg_generator
import logging
import time

logging.basicConfig(level=logging.INFO)

def send_sensor_value(host='127.0.0.1', port=5000):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        
        for i in range(5):
            data = msg_generator.generate_message()
            client_socket.sendall(data)
            time.sleep(1)
        
            # After sending sensor value, wait for a command from the server
            # receive_command_from_server(client_socket)
    except Exception as e:
        logging.error(f"Failed to send sensor value: {e}")
    finally:
        client_socket.close()

def receive_command_from_server(client_socket):
    try:
        data = client_socket.recv(1024)
        if data:
            command = commands_pb2.ControlCommand()
            command.ParseFromString(data)
            logging.info(f"Received command: id={command.id}, command={command.command}, motorPosition={command.motorPosition}")
            # Process the command as needed
    except Exception as e:
        logging.error(f"Error receiving command from server: {e}")

if __name__ == "__main__":
    # Example sensor value
    send_sensor_value()
