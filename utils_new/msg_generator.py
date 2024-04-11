import sys
import os

# Calculate the absolute path to the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the project root to the Python search path
sys.path.append(project_root)

# Now try importing your module
from message_formats import sensor_vals_pb2
import random

def create_sensor(name, id, value_range, include_value=True, include_switch=False):
    """Create and return a populated Sensor message."""
    sensor = sensor_vals_pb2.Sensor()
    sensor.name = name
    sensor.id = id
    if include_value:
        sensor.value = random.uniform(*value_range)  # Generate a random value within the range
    if include_switch:
        sensor.switchOn = random.choice([True, False])  # Randomly decide the switch state if included
    return sensor

def generate_message():
    sensor_data = sensor_vals_pb2.SensorData()

    # Define sensors with name, ID, value range, and whether to include the switchOn field
    sensors_config = [
        ("Temperature Sensor", 1, (20.0, 400.0), True, False),
        ("Pressure Sensor", 2, (1.0, 10.0), True, False),
        ("Switch", 3, None, False, True),
        ("StepperMotor", 4, (0.0, 90.0), True, False)
    ]

    # Populate the SensorData message
    for name, id, value_range, include_value, include_switch in sensors_config:
        sensor = create_sensor(name, id, value_range, include_value, include_switch)
        sensor_data.sensors.append(sensor)

    # Serialize the SensorData message to a binary string
    binary_data = sensor_data.SerializeToString()

    return binary_data

def main():
    
    binary_data = generate_message()
    # For demonstration purposes, print the serialized data's size
    print(f"Serialized SensorData size: {len(binary_data)} bytes")

if __name__ == "__main__":
    main()
