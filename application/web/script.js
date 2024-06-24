function sendCommand() {
    let commands = [];

    // Capture switch commands
    for (let i = 1; i <= 3; i++) {
        let switchState = document.querySelector(`input[name="switch_${i}"]:checked`);
        if (switchState) {
            commands.push({
                id: i + 6, // Assuming switches have IDs 7, 8, 9
                type: 'SWITCH',
                state: switchState.value
            });
        }
    }

    // Capture stepper motor commands
    for (let i = 1; i <= 3; i++) {
        let motorPosition = document.getElementById(`motor_position_${i}`).value;
        if (motorPosition !== '') {
            commands.push({
                id: i + 9, // Assuming stepper motors have IDs 10, 11, 12
                type: 'STEPPER_MOTOR',
                position: motorPosition
            });
        }
    }

    console.log('Sending commands:', commands);
    eel.send_commands_to_server(commands);
}

eel.expose(update_sensor_data);

function update_sensor_data(sensorData) {
    console.log('Received sensor data:', sensorData);  // Log the received data
    for (let sensorId in sensorData) {
        let sensor = sensorData[sensorId];
        console.log(`Updating sensor ${sensorId}:`, sensor);  // Log each sensor update
        let element = document.getElementById(`sensor_${sensorId}`);
        if (element) {
            console.log(`Element found for sensor ${sensorId}:`, element);  // Log the found element
            if (sensor.name === 'Switch') {
                element.innerText = sensor.switch_on ? 'On' : 'Off';
            } else {
                element.innerText = sensor.value;
            }
        } else {
            console.warn(`No element found for sensor ${sensorId}`);  // Warn if element is not found
        }
    }
}
