import time
import struct
from RF24 import RF24, RF24_PA_HIGH
from Sampling import *
import RPi.GPIO as GPIO
import threading

CSN_PIN = 0  
CE_PIN = 22
radio = RF24(CE_PIN, CSN_PIN)
LED1_PIN = 20
LED2_PIN = 21
Charge = 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED1_PIN, GPIO.OUT)
GPIO.setup(LED2_PIN, GPIO.OUT)
GPIO.setup(Charge, GPIO.OUT)

if not radio.begin():
    raise RuntimeError("radio hardware is not responding")

address = [b"1Node", b"2Node"]
radio_number = 1
radio.setPALevel(RF24_PA_HIGH)
radio.openWritingPipe(address[radio_number])
radio.payloadSize = 32

def check_battery():
    while True:
        vector = read_sensor_data()
        BAT = vector[-1]
        if BAT < 80:
            GPIO.output(Charge, GPIO.HIGH)
        else:
            GPIO.output(Charge, GPIO.LOW)
        time.sleep(100)

def main():
    radio.stopListening()
    while True:
        vector = read_sensor_data()
        print("Sensor Data:", vector)
        
        first_part = struct.pack("<8f", *vector[:8])
        start_timer = time.monotonic_ns()
        result1 = radio.write(first_part)
        end_timer = time.monotonic_ns()
        total_time_ms = (end_timer - start_timer) / 1000000
        print(f"Transmission Time: {total_time_ms} ms")
        second_part = struct.pack("<8f", *vector[8:], total_time_ms)
        result2 = radio.write(second_part)

        if not result1 or not result2:
            print("Transmission failed or timed out")
            GPIO.output(LED2_PIN, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(LED2_PIN, GPIO.LOW)
        else:
            print("Full vector transmitted! Time to Transmit:", f"{total_time_ms} ms. Sent: {vector}")
            GPIO.output(LED1_PIN, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(LED1_PIN, GPIO.LOW)
            
        time.sleep(0.5)  # Small delay to help with synchronization

if __name__ == "__main__":
    try:
        battery_thread = threading.Thread(target=check_battery)
        battery_thread.daemon = True
        battery_thread.start()
        main()
    except KeyboardInterrupt:
        print("Keyboard Interrupt detected. Powering down radio.")
        radio.powerDown()
        GPIO.cleanup()
