import random
from message_formats import sensor_vals_pb2


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
        ("Temperature Sensor", 2, (20.0, 400.0), True, False),
        ("Temperature Sensor", 3, (20.0, 400.0), True, False),
        ("Pressure Sensor", 4, (1.0, 10.0), True, False),
        ("Pressure Sensor", 5, (1.0, 10.0), True, False),
        ("Pressure Sensor", 6, (1.0, 10.0), True, False),
        ("Switch", 7, None, False, True),
        ("Switch", 8, None, False, True),
        ("Switch", 9, None, False, True),
        ("StepperMotor", 10, (0.0, 90.0), True, False),
        ("StepperMotor", 11, (0.0, 90.0), True, False),
        ("StepperMotor", 12, (0.0, 90.0), True, False)
    ]

    # Populate the SensorData message
    for name, id, value_range, include_value, include_switch in sensors_config:
        sensor = create_sensor(name, id, value_range, include_value, include_switch)
        sensor_data.sensors.append(sensor)

    # Serialize the SensorData message to a binary string
    binary_data = sensor_data.SerializeToString()

    return binary_data


def write_file(message: str):
    with open("dummyMessage.bin", "wb") as f:
        f.write(message)
    

def main():
    binary_data = generate_message()
    write_file(binary_data)


if __name__ == "__main__":
    main()
