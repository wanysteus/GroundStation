import json
import msg_parser

class Sensor:
    def __init__(self, name, sensor_id, value=None, switch_on=None):
        self.name = name
        self.sensor_id = sensor_id
        self.value = value
        self.switch_on = switch_on

    def update(self, value=None, switch_on=None):
        if value is not None:
            self.value = value
        if switch_on is not None:
            self.switch_on = switch_on

class TemperatureSensor(Sensor):
    def update(self, value=None, **kwargs):
        if value is not None:
            self.value = self.convert_temperature(value)
        super().update(**kwargs)

    @staticmethod
    def convert_temperature(value):
        # Conversion function for temperature
        return (value - 32) * 5.0 / 9.0 

class PressureSensor(Sensor):
    def update(self, value=None, **kwargs):
        if value is not None:
            self.value = self.convert_pressure(value)
        super().update(**kwargs)

    @staticmethod
    def convert_pressure(value):
        # Conversion function for pressure
        return value

class Battery(Sensor):
    def update(self, value=None, **kwargs):
        if value is not None:
            self.value = self.convert_voltage(value)
        super().update(**kwargs)

    @staticmethod
    def convert_voltage(value):
        # Conversion function for voltage
        return value

class Switch(Sensor):
    def update(self, value=None, **kwargs):
        super().update(**kwargs)

class StepperMotor(Sensor):
    def update(self, value=None, **kwargs):
        if value is not None:
            self.value = self.convert_degrees(value)
        super().update(**kwargs)

    @staticmethod
    def convert_degrees(value):
        # Conversion function for stepper valve position
        return value
    
class SensorManager:
    def __init__(self):
        self.sensors = {}

    def update_or_add_sensor(self, sensor_info):
        sensor_id = sensor_info['id']
        sensor_type = sensor_info['name']
        sensor_value = sensor_info.get('value')
        sensor_switch_on = sensor_info.get('switchOn')

        # Determine the type of sensor and create or update accordingly
        if sensor_id in self.sensors:
            sensor = self.sensors[sensor_id]
        else:
            if sensor_type == "Temperature Sensor":
                sensor = TemperatureSensor(sensor_type, sensor_id)
            elif sensor_type == "Pressure Sensor":
                sensor = PressureSensor(sensor_type, sensor_id)
            elif sensor_type == "Battery":
                sensor = Battery(sensor_type, sensor_id)
            elif sensor_type == "Switch":
                sensor = Switch(sensor_type, sensor_id)
            elif sensor_type == "Stepper Motor":
                sensor = StepperMotor(sensor_type, sensor_id)
            else:
                sensor = Sensor(sensor_type, sensor_id)  # Fallback to generic sensor
            self.sensors[sensor_id] = sensor

        # Update sensor data
        sensor.update(value=sensor_value, switch_on=sensor_switch_on)

    def update_from_json(self, json_data):
        sensor_data = json.loads(json_data)
        for sensor_info in sensor_data['sensors']:
            self.update_or_add_sensor(sensor_info)

    def get_sensor_data(self):
        sensor_data = {}
        for sensor_id, sensor in self.sensors.items():
            sensor_data[sensor_id] = {
                'name': sensor.name,
                'value': sensor.value,
                'switch_on': sensor.switch_on
            }
        return sensor_data

    def display_sensors(self):
        for sensor_id, sensor in self.sensors.items():
            print(f"    Sensor ID: {sensor_id}")
            print(f"    Name: {sensor.name}")
            if sensor.name == 'Switch':
                print(f"    SwitchOn: {sensor.switch_on}", end="\n\n")
            else: 
                print(f"    Value: {sensor.value}", end="\n\n")


def main():
    with open("dummyMessage.bin", "rb") as f:
        sensor_data = f.read()
    
    sensors_json = msg_parser.parse_sensor_data(sensor_data)

    sensors = SensorManager()

    sensors.update_from_json(sensors_json)

    # Display the state of all sensors managed by SensorManager
    sensors.display_sensors()

if __name__ == "__main__":
    main()
