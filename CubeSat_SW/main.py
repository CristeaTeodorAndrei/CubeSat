import time
import struct
from RF24 import RF24, RF24_PA_LOW
from Nominal import read_sensor_data
# Initialization of the RF24 module
CSN_PIN = 0  # GPIO8 aka CE0 on SPI bus 0: /dev/spidev0.0
CE_PIN = 22
radio = RF24(CE_PIN, CSN_PIN)

if not radio.begin():
    raise RuntimeError("radio hardware is not responding")

address = [b"1Node", b"2Node"]
radio_number = 1
radio.setPALevel(RF24_PA_LOW)  # RF24_PA_MAX is default
radio.openWritingPipe(address[radio_number])  # always uses pipe 0
radio.payloadSize = 32  # Set to maximum payload size supported by nRF24L01+



def transmit_data():
    radio.stopListening()  # put radio in TX mode
    while True:
        vector = read_sensor_data()
        
        # Split the vector into two parts
        first_part = struct.pack("<8f", *vector[:8])  # First 8 floats

        # Start timer
        start_timer = time.monotonic_ns()

        # Transmit the first part
        result1 = radio.write(first_part)

        # Measure end time
        end_timer = time.monotonic_ns()
        total_time_ms = (end_timer - start_timer) / 1000000  # Convert nanoseconds to microseconds

        # Include the time as the 16th float
        second_part = struct.pack("<8f", *vector[8:], total_time_ms)  # Last 7 floats and the time

        # Transmit the second part
        result2 = radio.write(second_part)

        if not result1 or not result2:
            print("Transmission failed or timed out")
        else:
            print(
                "Full vector transmitted! Time to Transmit:",
                f"{total_time_ms} ms. Sent: {vector}",
            )

        time.sleep(1)

if __name__ == "__main__":
    try:
        transmit_data()
    except KeyboardInterrupt:
        print("Keyboard Interrupt detected. Powering down radio.")
        radio.powerDown()
