import { configureStore } from '@reduxjs/toolkit';
import sensorReducer from './slices/sensorSlice';

const store = configureStore({
  reducer: {
    sensor: sensorReducer
  },
});

export default store;