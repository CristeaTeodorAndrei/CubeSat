import psutil
import time
import smbus2
import RPi.GPIO as GPIO

MPU9250_ADDRESS = 0x68
MPU9250_ACCEL_XOUT_H = 0x3B
MPU9250_ACCEL_YOUT_H = 0x3D
MPU9250_ACCEL_ZOUT_H = 0x3F
MPU9250_GYRO_XOUT_H = 0x43
MPU9250_GYRO_YOUT_H = 0x45
MPU9250_GYRO_ZOUT_H = 0x47
MPU9250_MAG_XOUT_L = 0x03
MPU9250_MAG_XOUT_H = 0x04
MPU9250_MAG_YOUT_L = 0x05
MPU9250_MAG_YOUT_H = 0x06
MPU9250_MAG_ZOUT_L = 0x07
MPU9250_MAG_ZOUT_H = 0x08
MPU9250_TEMP_OUT_H = 0x41
MPU9250_TEMP_OUT_L = 0x42
_REG_CONFIG = 0x00
_REG_SHUNTVOLTAGE = 0x01
_REG_BUSVOLTAGE = 0x02
_REG_POWER = 0x03
_REG_CURRENT = 0x04
_REG_CALIBRATION = 0x05

bus = smbus2.SMBus(1)
GPIO.setmode(GPIO.BCM)
packet_number = 0

class BusVoltageRange:
    RANGE_16V = 0x00
    RANGE_32V = 0x01

class Gain:
    DIV_1_40MV = 0x00
    DIV_2_80MV = 0x01
    DIV_4_160MV = 0x02
    DIV_8_320MV = 0x03

class ADCResolution:
    ADCRES_9BIT_1S = 0x00
    ADCRES_10BIT_1S = 0x01
    ADCRES_11BIT_1S = 0x02
    ADCRES_12BIT_1S = 0x03
    ADCRES_12BIT_2S = 0x09
    ADCRES_12BIT_4S = 0x0A
    ADCRES_12BIT_8S = 0x0B
    ADCRES_12BIT_16S = 0x0C
    ADCRES_12BIT_32S = 0x0D
    ADCRES_12BIT_64S = 0x0E
    ADCRES_12BIT_128S = 0x0F

class Mode:
    POWERDOW = 0x00
    SVOLT_TRIGGERED = 0x01
    BVOLT_TRIGGERED = 0x02
    SANDBVOLT_TRIGGERED = 0x03
    ADCOFF = 0x04
    SVOLT_CONTINUOUS = 0x05
    BVOLT_CONTINUOUS = 0x06
    SANDBVOLT_CONTINUOUS = 0x07

class INA219:
    def __init__(self, i2c_bus=1, addr=0x40):
        self.bus = smbus2.SMBus(i2c_bus)
        self.addr = addr
        self._cal_value = 0
        self._current_lsb = 0
        self._power_lsb = 0
        self.set_calibration_16V_5A()

    def read(self, address):
        data = self.bus.read_i2c_block_data(self.addr, address, 2)
        return (data[0] * 256) + data[1]

    def write(self, address, data):
        temp = [0, 0]
        temp[1] = data & 0xFF
        temp[0] = (data & 0xFF00) >> 8
        self.bus.write_i2c_block_data(self.addr, address, temp)

    def set_calibration_16V_5A(self):
        self._current_lsb = 0.1524  # Current LSB = 100uA per bit
        self._cal_value = 26868
        self._power_lsb = 0.003048  # Power LSB = 2mW per bit
        self.write(_REG_CALIBRATION, self._cal_value)
        self.bus_voltage_range = BusVoltageRange.RANGE_16V
        self.gain = Gain.DIV_2_80MV
        self.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
        self.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
        self.mode = Mode.SANDBVOLT_CONTINUOUS
        self.config = (
            self.bus_voltage_range << 13
            | self.gain << 11
            | self.bus_adc_resolution << 7
            | self.shunt_adc_resolution << 3
            | self.mode
        )
        self.write(_REG_CONFIG, self.config)

    def getShuntVoltage_mV(self):
        self.write(_REG_CALIBRATION, self._cal_value)
        value = self.read(_REG_SHUNTVOLTAGE)
        if value > 32767:
            value -= 65535
        return value * 0.01

    def getBusVoltage_V(self):
        self.write(_REG_CALIBRATION, self._cal_value)
        self.read(_REG_BUSVOLTAGE)
        return (self.read(_REG_BUSVOLTAGE) >> 3) * 0.004

    def getCurrent_mA(self):
        value = self.read(_REG_CURRENT)
        if value > 32767:
            value -= 65535
        return value * self._current_lsb

    def getPower_W(self):
        self.write(_REG_CALIBRATION, self._cal_value)
        value = self.read(_REG_POWER)
        if value > 32767:
            value -= 65535
        return value * self._power_lsb

def read_word_2c(reg):
    high = bus.read_byte_data(MPU9250_ADDRESS, reg)
    low = bus.read_byte_data(MPU9250_ADDRESS, reg + 1)
    value = (high << 8) + low
    if (value >= 0x8000):
        value = -((65535 - value) + 1)
    return value

def read_cpu_temperature():
    try:
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            temp = int(f.read()) / 1000.0
            return temp
    except FileNotFoundError:
        return None

def convert_accel(raw_value):
    sensibility = 2.0 / 32768.0
    return raw_value * sensibility

def convert_gyro(raw_value):
    sensibility = 500.0 / 32768.0
    return raw_value * sensibility

def convert_mag(raw_value):
    sensibility = 4800.0 / 32768.0
    return raw_value * sensibility

ina219 = INA219(i2c_bus=1, addr=0x43)

def read_sensor_data():
    bus_voltage = ina219.getBusVoltage_V()
    current = -ina219.getCurrent_mA()
    power = ina219.getPower_W()
    p = (bus_voltage - 3) / 1.2 * 100

    accel_x = read_word_2c(MPU9250_ACCEL_XOUT_H)
    accel_y = read_word_2c(MPU9250_ACCEL_YOUT_H)
    accel_z = read_word_2c(MPU9250_ACCEL_ZOUT_H)

    gyro_x = read_word_2c(MPU9250_GYRO_XOUT_H)
    gyro_y = read_word_2c(MPU9250_GYRO_YOUT_H)
    gyro_z = read_word_2c(MPU9250_GYRO_ZOUT_H)

    print(f"Gyro raw values: x={gyro_x}, y={gyro_y}, z={gyro_z}")

    mag_x = read_word_2c(MPU9250_MAG_XOUT_L) / 1000
    mag_y = read_word_2c(MPU9250_MAG_YOUT_L) / 1000
    mag_z = read_word_2c(MPU9250_MAG_ZOUT_L) / 1000

    vector = [
        round(read_cpu_temperature(), 3),
        round(psutil.cpu_percent(), 3),
        round(bus_voltage, 3),
        round(current / 1000, 3),
        round(power, 3),
        round(convert_accel(accel_x), 3),
        round(convert_accel(accel_y), 3),
        round(convert_accel(accel_z), 3),
        round(convert_gyro(gyro_x), 3),
        round(convert_gyro(gyro_y), 3),
        round(convert_gyro(gyro_z), 3),
        round(convert_mag(mag_x), 3),
        round(convert_mag(mag_y), 3),
        round(convert_mag(mag_z), 3),
        round(p, 3)
    ]

    return vector

# Test the function
print(read_sensor_data())
