import socket
import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
from message_formats import commands_pb2
import msg_generator
import time


def send_sensor_value(iterations, host='127.0.0.1', port=5000):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    
    for i in range(iterations):
        data = msg_generator.generate_message()
        client_socket.sendall(data)
        receive_command_from_server(client_socket)
        time.sleep(1)
        

    client_socket.close()


def receive_command_from_server(client_socket):
    try:
        data = client_socket.recv(1024)
        if data:
            command = commands_pb2.ControlCommand()
            command.ParseFromString(data)
            print(f"Received command: id={command.id}, command={command.command}, motorPosition={command.motorPosition}")
            # Process the command as needed
    except Exception as e:
        print(f"Error receiving command from server: {e}")



if __name__ == "__main__":
    
    send_sensor_value(5)
