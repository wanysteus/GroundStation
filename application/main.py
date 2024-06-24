import socket
import threading
import eel
from message_formats import sensor_vals_pb2
from message_formats import commands_pb2
import logging
import sensors_new

logging.basicConfig(level=logging.INFO)

eel.init('c:/Users/nickl/OneDrive/Dokument/GitHub/ground-control/application/web')  # Update this path


clients = []

def start_server(host='0.0.0.0', port=5000):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    logging.info(f"Server listening on {host}:{port}")
    
    while True:
        client_socket, addr = server_socket.accept()
        clients.append(client_socket)
        logging.info(f"Accepted connection from {addr}")
        eel.setConnectionStatus(True)  # Set connection status to green
        threading.Thread(target=handle_client_connection, args=(client_socket,)).start()

def handle_client_connection(client_socket):
    sensors = sensors_new.SensorManager()
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            receive_sensor_data(sensors, data)
    except Exception as e:
        logging.error(f"Error handling client connection: {e}")
    finally:
        client_socket.close()
        clients.remove(client_socket)
        if not clients:
            eel.setConnectionStatus(False)  # Set connection status to red

def receive_sensor_data(sensors, data):
    sensors_json = sensors_new.msg_parser.parse_sensor_data(data)
    sensors.update_from_json(sensors_json)
    # sensors.display_sensors() # Troubleshooting, displays sensor data in terminal
    
    # Send the updated sensor data to the web interface

    # logging.info(f"Sending sensor data to web: {sensors.get_sensor_data()}")  # Log the data being sent
    eel.update_sensor_data(sensors.get_sensor_data())


@eel.expose
def send_command_to_client(command_id, command_type, motor_position=None):
    command = commands_pb2.ControlCommand()
    command.id = int(command_id)
    command.command = commands_pb2.CommandType.Value(command_type)
    if motor_position is not None:
        command.motorPosition = int(motor_position)

    data = command.SerializeToString()
    for client_socket in clients:
        try:
            client_socket.sendall(data)
            logging.info(f"Sent command: id={command.id}, command={command.command}, motorPosition={command.motorPosition}")
        except Exception as e:
            logging.error(f"Error sending command to client: {e}")

@eel.expose
def send_commands_to_server(commands):
    for command in commands:
        if command['type'] == 'SWITCH':
            send_command_to_client(command['id'], 'OPEN' if command['state'] == 'open' else 'CLOSE')
        elif command['type'] == 'STEPPER_MOTOR':
            send_command_to_client(command['id'], 'SET_MOTOR_POSITION', command['position'])


if __name__ == "__main__":
    threading.Thread(target=start_server).start()
    eel.start('index.html', size=(1000, 800))
