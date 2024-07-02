// Expose the function to Eel
eel.expose(update_sensor_data);

let temperatureData = { labels: [], datasets: [] };
let pressureData = { labels: [], datasets: [] };
let switchData = { labels: [], datasets: [] };
let stepperMotorData = { labels: [], datasets: [] };

let temperatureChart, pressureChart, switchChart, stepperMotorChart;

const sensorColors = {
    1: 'rgba(255, 99, 132, 0.6)',
    2: 'rgba(54, 162, 235, 0.6)',
    3: 'rgba(75, 192, 192, 0.6)',
    4: 'rgba(153, 102, 255, 0.6)',
    5: 'rgba(255, 159, 64, 0.6)',
    6: 'rgba(255, 206, 86, 0.6)',
    7: 'rgba(231, 233, 237, 0.6)',
    8: 'rgba(56, 86, 255, 0.6)',
    9: 'rgba(77, 75, 192, 0.6)',
    10: 'rgba(54, 235, 162, 0.6)',
    11: 'rgba(132, 99, 255, 0.6)',
    12: 'rgba(255, 64, 159, 0.6)'
};

function initializeCharts() {
    const ctxTemp = document.getElementById('temperatureChart').getContext('2d');
    const ctxPressure = document.getElementById('pressureChart').getContext('2d');
    const ctxSwitch = document.getElementById('switchChart').getContext('2d');
    const ctxStepperMotor = document.getElementById('stepperMotorChart').getContext('2d');

    temperatureChart = new Chart(ctxTemp, { type: 'line', data: temperatureData });
    pressureChart = new Chart(ctxPressure, { type: 'line', data: pressureData });
    switchChart = new Chart(ctxSwitch, { type: 'line', data: switchData });
    stepperMotorChart = new Chart(ctxStepperMotor, { type: 'line', data: stepperMotorData });
}

function addSensorData(data, label, dataset) {
    if (data.labels.length >= 30) {
        data.labels.shift();
        data.datasets.forEach(dataset => dataset.data.shift());
    }

    data.labels.push(label);

    for (const [sensorId, sensorValue] of Object.entries(dataset)) {
        let datasetEntry = data.datasets.find(d => d.label === `Sensor ${sensorId}`);
        if (datasetEntry) {
            datasetEntry.data.push(sensorValue);
        } else {
            let newDataset = {
                label: `Sensor ${sensorId}`,
                data: Array(data.labels.length).fill(null),
                borderColor: sensorColors[sensorId],
                backgroundColor: sensorColors[sensorId],
                fill: false
            };
            newDataset.data[newDataset.data.length - 1] = sensorValue;
            data.datasets.push(newDataset);
        }
    }

    // Ensure all datasets have the same length
    data.datasets.forEach(dataset => {
        while (dataset.data.length < data.labels.length) {
            dataset.data.push(null);
        }
    });
}

function updateCharts(sensorData) {
    const timestamp = new Date().toLocaleTimeString();

    const temperatureDataset = {};
    const pressureDataset = {};
    const switchDataset = {};
    const stepperMotorDataset = {};

    for (let sensorId in sensorData) {
        let sensor = sensorData[sensorId];
        if (sensor.name.includes('Temperature')) {
            temperatureDataset[sensorId] = sensor.value;
        } else if (sensor.name.includes('Pressure')) {
            pressureDataset[sensorId] = sensor.value;
        } else if (sensor.name.includes('Switch')) {
            switchDataset[sensorId] = sensor.switch_on ? 1 : 0;
        } else if (sensor.name.includes('Stepper Motor')) {
            stepperMotorDataset[sensorId] = sensor.value;
        }
    }

    addSensorData(temperatureData, timestamp, temperatureDataset);
    addSensorData(pressureData, timestamp, pressureDataset);
    addSensorData(switchData, timestamp, switchDataset);
    addSensorData(stepperMotorData, timestamp, stepperMotorDataset);

    temperatureChart.update();
    pressureChart.update();
    switchChart.update();
    stepperMotorChart.update();
}

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
    updateCharts(sensorData);
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

// Function to handle tab switching
function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

// Initialize charts when the page loads
window.onload = function() {
    initializeCharts();
}

// Example usage:
// setConnectionStatus(true); // Set status to connected

// Expose the function to Python via Eel
eel.expose(setConnectionStatus);
