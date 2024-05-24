import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QTextEdit
from PyQt5.QtCore import Qt, QTimer
import threading
import serial.tools.list_ports
import csv
import time

# Find the port to which the Arduino is connected
def cautare_port():
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        if "CH340" in port.description:
            return port.device
    return None

# Function to read data from Arduino
def citeste_date(data_list, stop_event):
    buffer = ""
    port = None

    while not stop_event.is_set():
        try:
            if port is None or not port.is_open:
                port_device = cautare_port()
                if port_device:
                    port = serial.Serial(port_device, 115200, timeout=1)
                    print("Connected to port:", port_device)
                    buffer = ""  # Clear the buffer on reconnection
                else:
                    print("No port found, retrying in 5 seconds...")
                    time.sleep(5)
                    continue
                    buffer = ""  # Clear the buffer on reconnection

            buffer += port.read(port.in_waiting or 1024).decode('utf-8')
            if '\n' in buffer:
                lines = buffer.split('\n')
                for line in lines[:-1]:
                    if line.strip():
                        numbers = [float(x) for x in line.split()]
                        data_list.append(numbers)
                buffer = lines[-1]
        except (serial.SerialException, OSError) as e:
            print("Lost connection, retrying in 5 seconds...")
            if port and port.is_open:
                port.close()
            port = None
        except Exception as e:
            print("Unexpected error:", str(e))
            if port and port.is_open:
                port.close()
            port = None

class Raw(QMainWindow):
    def __init__(self, main_window_reference):
        super().__init__()
        self.data_list = []
        self.saving_data = False
        self.stop_event = threading.Event()

        # Start data reading thread
        self.start_data_thread()

        # Setează titlul ferestrei
        self.setWindowTitle("Terminal Emulator")

        # Creează butoanele de ieșire și revenire
        self.exit_button = QPushButton("Exit", self)
        self.exit_button.setStyleSheet("background-color: #c0392b; color: white; border-radius: 15px; font-weight: bold;")
        self.exit_button.clicked.connect(self.close_application)

        self.back_button = QPushButton("Main Page", self)
        self.back_button.setStyleSheet("background-color: #c0392b; color: white; border-radius: 15px; font-weight: bold;")
        self.back_button.clicked.connect(self.return_to_main_page)

        self.save_button = QPushButton("Save", self)
        self.save_button.setStyleSheet("background-color: #27ae60; color: white; border-radius: 15px; font-weight: bold;")
        self.save_button.clicked.connect(self.toggle_save_data)

        # Creează un layout orizontal pentru butoanele de revenire și ieșire
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.exit_button)

        # Referința către fereastra principală
        self.main_window_reference = main_window_reference

        # Creează un layout principal de tip QVBoxLayout
        main_layout = QVBoxLayout()

        # Creează zona de afișare a terminalului
        self.terminal_output = QTextEdit()
        self.terminal_output.setReadOnly(True)
        self.terminal_output.setStyleSheet("background-color: black; color: white; font-family: monospace; font-size: 12pt;")

        # Adaugă componentele terminalului la layout-ul principal
        main_layout.addWidget(self.terminal_output)
        main_layout.addLayout(button_layout)

        # Creează un widget central pentru a avea fundalul dorit
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #1E1E1E;")  # Setează culoarea fundalului widget-ului central
        central_widget.setLayout(main_layout)

        # Setează widget-ul central al ferestrei
        self.setCentralWidget(central_widget)

        # Face butoanele mai groase și le plasează în stânga și în dreapta maxim
        self.back_button.setFixedSize(100, 50)
        self.save_button.setFixedSize(100, 50)
        self.exit_button.setFixedSize(100, 50)
        button_layout.setAlignment(self.back_button, Qt.AlignLeft)
        button_layout.setAlignment(self.save_button, Qt.AlignCenter)
        button_layout.setAlignment(self.exit_button, Qt.AlignRight)

        # Afișează fereastra full screen după ce se inițiază toate componentele
        self.showFullScreen()

        # Timer to update terminal output
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_terminal_output)
        self.timer.start(1000)  # Update every second

    def start_data_thread(self):
        self.thread = threading.Thread(target=citeste_date, args=(self.data_list, self.stop_event))
        self.thread.daemon = True
        self.thread.start()

    def toggle_save_data(self):
        if self.saving_data:
            self.saving_data = False
            self.save_button.setText("Save")
            self.save_button.setStyleSheet("background-color: #27ae60; color: white; border-radius: 15px; font-weight: bold;")
        else:
            self.saving_data = True
            self.save_button.setText("STOP")
            self.save_button.setStyleSheet("background-color: #e74c3c; color: white; border-radius: 15px; font-weight: bold;")
            self.save_data_to_csv()

    def save_data_to_csv(self):
        if not self.saving_data:
            return

        with open("data.csv", "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerows(self.data_list)

        # Schedule next save if still saving
        if self.saving_data:
            QTimer.singleShot(1000, self.save_data_to_csv)  # Save every second

    def update_terminal_output(self):
        # Clear terminal output
        self.terminal_output.clear()

        # Display the data list in the terminal output with index
        for index, data in enumerate(self.data_list, start=1):
            data_str = '{}. [{}]'.format(index, ', '.join(map(str, data)))
            self.terminal_output.append(data_str)
            self.terminal_output.append("\n")  # Ensure a new line after each array

    def return_to_main_page(self):
        # Afișează fereastra principală și ascunde fereastra curentă
        self.main_window_reference.show()
        self.hide()

    def close_application(self):
        self.stop_event.set()
        self.thread.join()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Raw(None)
    window.showFullScreen()
    sys.exit(app.exec_())
