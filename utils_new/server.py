import socket
import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
from message_formats import sensor_vals_pb2
import sensors_new



def handle_client_connection(client_socket):
    sensors = sensors_new.SensorManager()
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            # Assuming the received data is a SensorValue message
            sensors_json = sensors_new.msg_parser.parse_sensor_data(data)
            sensors.update_from_json(sensors_json)
            sensors.display_sensors()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

def start_server(host='0.0.0.0', port=5000):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")
    
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
        handle_client_connection(client_socket)

if __name__ == "__main__":
    start_server()
