import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  sensors: [
    {id: 0, name: "Temperature Sensor", value: 0},
    {id: 1, name: "Temperature Sensor", value: 0},
    {id: 2, name: "Temperature Sensor", value: 0},
    {id: 3, name: "Pressure Sensor", value: 0},
    {id: 4, name: "Pressure Sensor", value: 0},
    {id: 5, name: "Pressure Sensor", value: 0},
    {id: 6, name: "Switch", value: false},
    {id: 7, name: "Switch", value: false},
    {id: 8, name: "Switch", value: false},
    {id: 9, name: "StepperMotor", value: 0},
    {id: 10, name: "StepperMotor", value: 0},
    {id: 11, name: "StepperMotor", value: 0},
  ],
};

export const sensorSlice = createSlice({
  name: 'sensor',
  initialState,
  reducers: {
    updateSensorValue: (state, action) => {
      const updatedSensors = state.sensors.map((sensor) => {
        if (sensor.id === action.payload.id) return action.payload;
        return sensor;
      });
      state.sensors = updatedSensors;
    },
  }
});

export const { updateSensorValue } = sensorSlice.actions;

export default sensorSlice.reducer;