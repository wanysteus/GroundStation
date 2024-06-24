document.getElementById('command_type').addEventListener('change', function() {
    var motorPositionDiv = document.getElementById('motor_position_div');
    if (this.value === 'SET_MOTOR_POSITION') {
        motorPositionDiv.style.display = 'block';
    } else {
        motorPositionDiv.style.display = 'none';
    }
});

function sendCommand() {
    let commandId = document.getElementById('command_id').value;
    let commandType = document.getElementById('command_type').value;
    let motorPosition = document.getElementById('motor_position').value;
    
    if (commandType === 'SET_MOTOR_POSITION' && motorPosition === '') {
        alert('Please enter motor position');
        return;
    }

    motorPosition = motorPosition || null;
    
    eel.send_command_to_client(commandId, commandType, motorPosition);
}

eel.expose(update_sensor_data);
function update_sensor_data(message) {
    let sensorDataDisplay = document.getElementById('sensor_data_display');
    let newData = document.createElement('div');
    newData.innerText = JSON.stringify(message, null, 2);  // Formatting JSON data for better readability
    sensorDataDisplay.appendChild(newData);
}
