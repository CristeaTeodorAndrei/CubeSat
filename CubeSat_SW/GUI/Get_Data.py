import serial.tools.list_ports
import threading

# Caută portul la care este conectat Arduino-ul
def cautare_port():
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports):
        if "Arduino" in desc:
            return port

# Funcție pentru citirea datelor de la Arduino
def citeste_date(port):
    with serial.Serial(port, 9600, timeout=1) as ser:
        while True:
            line = ser.readline().decode().strip()
            print(line)

if __name__ == "__main__":
    port = cautare_port()
    if port:
        thread = threading.Thread(target=citeste_date, args=(port,))
        thread.daemon = True
        thread.start()
        thread.join()
    else:
        print("Nema.")
