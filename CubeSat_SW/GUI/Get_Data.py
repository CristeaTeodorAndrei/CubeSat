import serial.tools.list_ports
import threading
import time

# Find the port to which the Arduino is connected
def cautare_port():
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        if "CH340" in port.description:
            return port.device
    return None

# Function to read data from Arduino
def citeste_date(port, data_list):
    with serial.Serial(port, 115200, timeout=1) as ser:
        while True:
            line = ser.readline().decode().strip()
            if line:
                try:
                    # Split the line into individual string numbers, then convert them to floats
                    numbers = [float(x) for x in line.split()]
                    data_list.append(numbers)
                except ValueError as e:
                    print(f"Error converting data to float: {e}")
                    continue

if __name__ == "__main__":
    data_list = []
    port = cautare_port()
    if port:
        thread = threading.Thread(target=citeste_date, args=(port, data_list))
        thread.daemon = True
        thread.start()

    #     try:
    #         while True:
    #             print(data_list)
    #             time.sleep(1)  # Print the array every second
    #     except KeyboardInterrupt:
    #         print("Stopped by user")
    # else:
    #     print("No port found.")
