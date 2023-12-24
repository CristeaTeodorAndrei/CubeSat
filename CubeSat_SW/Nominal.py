import smbus2
import psutil
import time
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

bus = smbus2.SMBus(1)
GPIO.setmode(GPIO.BCM)
packet_number = 0


def read_word(reg):
    high = bus.read_byte_data(MPU9250_ADDRESS, reg)
    low = bus.read_byte_data(MPU9250_ADDRESS, reg + 1)
    value = (high << 8) + low
    return value

def read_cpu_temperature():
    # Returnează temperatura CPU-ului în grade Celsius
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
    # Sensibilitatea magnetometrului pentru gama +/- 4800uT
    sensibility = 4800.0 / 32768.0
    return raw_value * sensibility

def read_sensor_data():

    global packet_number
    packet_number += 1

    accel_x = read_word(MPU9250_ACCEL_XOUT_H)
    accel_y = read_word(MPU9250_ACCEL_YOUT_H)
    accel_z = read_word(MPU9250_ACCEL_ZOUT_H)
    gyro_x = read_word(MPU9250_GYRO_XOUT_H)
    gyro_y = read_word(MPU9250_GYRO_YOUT_H)
    gyro_z = read_word(MPU9250_GYRO_ZOUT_H)
    mag_x = read_word(MPU9250_MAG_XOUT_L)
    mag_y = read_word(MPU9250_MAG_YOUT_L)
    mag_z = read_word(MPU9250_MAG_ZOUT_L)

    return {
         packet_number,
         hex(round(read_cpu_temperature(), 3)),
         hex(round(psutil.cpu_percent(), 3)),
         hex(round(convert_accel(accel_x), 3)),
         hex(round(convert_accel(accel_y), 3)),
         hex(round(convert_accel(accel_z), 3)),
         hex(round(convert_gyro(gyro_x), 3)),
         hex(round(convert_gyro(gyro_y), 3)),
         hex(round(convert_gyro(gyro_z), 3)),
         hex(round(convert_mag(mag_x), 3)),
         hex(round(convert_mag(mag_y), 3)),
         hex(round(convert_mag(mag_z), 3))
    }

def main():
    try:
        while True:
            sensor_data = read_sensor_data()
            for value in sensor_data.values():
                print(value)


    except KeyboardInterrupt:
        print("Kill it!")
        GPIO.cleanup()

if _name_ == "_main_":
    main()