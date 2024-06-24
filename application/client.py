import socket
import threading
from message_formats import sensor_vals_pb2
from message_formats import commands_pb2
import logging
import random
import time

logging.basicConfig(level=logging.INFO)

# Initialize sensor data
sensor_data = {
    'temperature': [random.uniform(20.0, 100.0) for _ in range(3)],
    'pressure': [random.uniform(1.0, 10.0) for _ in range(3)],
    'switch': [random.choice([True, False]) for _ in range(3)],
    'stepper_motor': [random.uniform(0, 180) for _ in range(3)]
}

def generate_sensor_data():
    sensor_data_pb = sensor_vals_pb2.SensorData()

    # Generate random temperature and pressure values
    for i in range(3):
        sensor = sensor_data_pb.sensors.add()
        sensor.id = i + 1
        sensor.name = "Temperature Sensor"
        sensor.value = random.uniform(20.0, 100.0)
        sensor_data['temperature'][i] = sensor.value

    for i in range(3):
        sensor = sensor_data_pb.sensors.add()
        sensor.id = i + 4
        sensor.name = "Pressure Sensor"
        sensor.value = random.uniform(1.0, 10.0)
        sensor_data['pressure'][i] = sensor.value

    # Add switch and stepper motor values
    for i in range(3):
        sensor = sensor_data_pb.sensors.add()
        sensor.id = i + 7
        sensor.name = "Switch"
        sensor.switchOn = sensor_data['switch'][i]  # Use correct field for switch state

    for i in range(3):
        sensor = sensor_data_pb.sensors.add()
        sensor.id = i + 10
        sensor.name = "Stepper Motor"
        sensor.value = sensor_data['stepper_motor'][i]

    return sensor_data_pb.SerializeToString()

def send_sensor_value(client_socket):
    try:
        while True:
            data = generate_sensor_data()
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
                # Update switch and stepper motor states based on the command
                if command.id in range(7, 10):  # Switches
                    sensor_data['switch'][command.id - 7] = command.command == commands_pb2.CommandType.OPEN
                elif command.id in range(10, 13):  # Stepper Motors
                    sensor_data['stepper_motor'][command.id - 10] = command.motorPosition
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
