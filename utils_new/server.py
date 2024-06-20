import socket
import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
from message_formats import commands_pb2
import sensors_new


def handle_client_connection(client_socket):
    sensors = sensors_new.SensorManager()
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            # Assuming the received data is a SensorValue message
            receive_sensor_data(sensors, data)

            send_command_to_client(client_socket)


    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

def receive_sensor_data(sensors, data):
    sensors_json = sensors_new.msg_parser.parse_sensor_data(data)
    sensors.update_from_json(sensors_json)
    sensors.display_sensors()


def send_command_to_client(client_socket):
    try:
        command = commands_pb2.ControlCommand()
        command.id = 12
        command.command = commands_pb2.CommandType.SET_MOTOR_POSITION
        command.motorPosition = 100  # Example motor position

        data = command.SerializeToString()
        client_socket.sendall(data)
        print(f"Sent command: id={command.id}, command={command.command}, motorPosition={command.motorPosition}")
    except Exception as e:
        print(f"Error sending command to client: {e}")


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
