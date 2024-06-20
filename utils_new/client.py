import socket
import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
import msg_generator
import time


def send_sensor_value(iterations, host='127.0.0.1', port=5000):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    
    for i in range(iterations):
        data = msg_generator.generate_message()
        client_socket.sendall(data)
        time.sleep(1)

    client_socket.close()

if __name__ == "__main__":
    
    send_sensor_value(20)
