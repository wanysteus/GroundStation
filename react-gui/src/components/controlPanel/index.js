import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { updateSensorValue } from '../../state/slices/sensorSlice'

const ControlPanel = () => {
  const dispatch = useDispatch()
  const sensors = useSelector(state => state.sensor.sensors)

  return (

    <div className='flex-col gap-5 m-2 p-2 bg-stone-200 border-2 border-gray-900 rounded-md'>
      <div className='flex flex-row gap-5'>
        <button className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
        onClick={() => dispatch(updateSensorValue({...sensors[7], value: !sensors[7].value}))}>
              switch 1: { sensors[7].value ? 'ON' : 'OFF' }
        </button>
        <button className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
        onClick={() => dispatch(updateSensorValue({...sensors[8], value: !sensors[8].value}))}>
              switch 2: { sensors[8].value ? 'ON' : 'OFF'}
        </button>
      </div>

      <div className='flex flex-row gap-5 mt-2'>
        <button className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
        onClick={() => dispatch(updateSensorValue({...sensors[9], value: sensors[9].value + 1}))}>
              stepper 1: { sensors[9].value }
        </button>
        <button className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
        onClick={() => dispatch(updateSensorValue({...sensors[10], value: sensors[10].value + 1}))}>
              stepper 2: { sensors[10].value }
        </button>
      </div>

      <div className='flex flex-row gap-5 mt-2'>
        <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        onClick={() => dispatch(updateSensorValue({...sensors[0], value: sensors[0].value + 1}))}>
              temp 1: { sensors[0].value }
        </button>
        <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        onClick={() => dispatch(updateSensorValue({...sensors[1], value: sensors[1].value + 1}))}>
              temp 2: { sensors[1].value }
        </button>
      </div>
    </div>
  )
}

export default ControlPanel