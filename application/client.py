import socket
import threading
from message_formats import sensor_vals_pb2
from message_formats import commands_pb2
import msg_generator
import logging
import time

logging.basicConfig(level=logging.INFO)

def send_sensor_value(client_socket):
    try:
        while True:
            data = msg_generator.generate_message()
            client_socket.sendall(data)
            time.sleep(1)
    except Exception as e:
        logging.error(f"Failed to send sensor value: {e}")

def receive_command_from_server(client_socket):
    try:
        while True:
            data = client_socket.recv(1024)
            if data:
                command = commands_pb2.ControlCommand()
                command.ParseFromString(data)
                logging.info(f"Received command: id={command.id}, command={command.command}, motorPosition={command.motorPosition}")
                # Process the command as needed
    except Exception as e:
        logging.error(f"Error receiving command from server: {e}")

def main(host='127.0.0.1', port=5000):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        
        threading.Thread(target=send_sensor_value, args=(client_socket,)).start()
        threading.Thread(target=receive_command_from_server, args=(client_socket,)).start()
        
    except Exception as e:
        logging.error(f"Failed to connect to server: {e}")
    # finally block is not necessary because threads will handle socket closure

if __name__ == "__main__":
    main()
