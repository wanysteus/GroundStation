import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
from message_formats import sensor_vals_pb2
import json

'''
Parses binary message to .json.

Current message format from sensor_vals.proto

Currently reads binary message from file, in future implementations this will be read from serialwrapper.py or another implementation 
of serial communication.
'''

def parse_sensor_data(binary_data):
    """Parse binary sensor data into a JSON string."""
    # Create a SensorData message object
    sensor_data = sensor_vals_pb2.SensorData()
    
    # Deserialize the binary data
    sensor_data.ParseFromString(binary_data)
    
    # Convert to a dictionary
    sensor_data_dict = {"sensors": []}
    for sensor in sensor_data.sensors:
        # Each sensor is a dictionary
        sensor_dict = {
            "name": sensor.name,
            "id": sensor.id,
            "value": sensor.value,
        }
        # Only add 'switchOn' if it's present
        if sensor.HasField("switchOn"):
            sensor_dict["switchOn"] = sensor.switchOn
        sensor_data_dict["sensors"].append(sensor_dict)
    
    # Convert dictionary to JSON
    sensor_json = json.dumps(sensor_data_dict, indent=4)
    return sensor_json

def main():
    # For demonstration, we'll assume binary_data is read from a file
    with open('dummyMessage.bin', 'rb') as file:
        binary_data = file.read()
    
    sensor_json = parse_sensor_data(binary_data)
    print(sensor_json)

if __name__ == "__main__":
    main()
