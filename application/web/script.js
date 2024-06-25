// Expose the function to Eel
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

// Functions to update connection status
function setConnectionStatus(isConnected) {
    let statusIndicator = document.getElementById('status-indicator');
    if (statusIndicator) {
        if (isConnected) {
            statusIndicator.classList.remove('red');
            statusIndicator.classList.add('green');
        } else {
            statusIndicator.classList.remove('green');
            statusIndicator.classList.add('red');
        }
    } else {
        console.error('Status indicator element not found');
    }
}

// Function to update slider value display
function updateSliderValue(motorId, value) {
    document.getElementById(`motor_position_${motorId}_value`).innerText = value;
}

// Example usage:
// setConnectionStatus(true); // Set status to connected

// Expose the function to Python via Eel
eel.expose(setConnectionStatus);
