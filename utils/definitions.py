
SEPARATOR = [10] #"\n"


#The IDs are no longer updated. do not use
#engine commands
ID_SET_POWER_MODE_EC = 0x22
ID_SET_ENGINE_STATE_EC = 0x23
ID_FIRE_ROCKET_EC = 0x2F
#engine returns
ID_SOFTWARE_STATE_EC = 0x30
ID_HARDWARE_STATE_EC =  0x31
ID_RETURN_POWER_MODE_EC = 0x32
ID_RETURN_ENGINE_STATE_EC = 0x33
ID_FIRE_ROCKET_CONFIRMATION_EC = 0x3F

#flight commands
ID_TIME_SYNC_FC = 0x10
ID_SET_POWER_MODE_FC =0x11
ID_SET_RADIO_EQUIPMENT_FC = 0x12
ID_SET_PARACHUTE_OUTPUT_FC = 0x13
ID_SET_DATA_LOGGING_FC = 0x14
ID_DUMP_FLASH_FC = 0x15
ID_HANDSHAKE = 0x16

#flight returns
ID_RETURN_TIME_SYNC_FC = 0x20
ID_RETURN_POWER_MODE_FC = 0x21
ID_RETURN_RADIO_EQUIPMENT_FC = 0x22
ID_RETURN_PARACHUTE_OUTPUT_FC = 0x23
ID_ONBOARD_BATTERY_VOLTAGE_FC = 0x24
ID_GNSS_DATA_FC = 0x25
ID_FLIGHT_CONTROLLER_STATUS_FC = 0x26
ID_RETURN_SET_DATA_LOGGING_FC = 0x27
ID_RETURN_DUMP_FLASH_FC = 0x28
ID_RETURN_HANDSHAKE = 0x29

#flight telemetry
ID_MS_SINCE_BOOT_FC = 0x50
ID_US_SINCE_BOOT_FC = 0x51
ID_CURRENT_TIME = 0x52
ID_GNSS_DATA_1_FC = 0x53
ID_GNSS_DATA_2_FC =0x54
ID_INSIDE_TEMPERATURE_FC = 0x55
ID_INSIDE_PRESSURE_FC = 0x56
ID_IMU_1_FC = 0x57
ID_IMU_2_FC = 0x58
ID_EXTERNAL_TEMPERATURE_FC = 0x59
ID_AIR_SPEED_FC = 0x5A
ID_ONBOARD_BATTERY_VOLTAGE_TM_FC = 0x5B
ID_FLIGHT_CONTROLLER_STATUS_TM_FC = 0x5C



ID_LOCAL_TIMESTAMP = 0xFF # timestamp for the backup file
INFLUX_NAME = "mjollnir"