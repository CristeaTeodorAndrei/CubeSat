import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QTextEdit, QSizePolicy
from PyQt5.QtCore import Qt, QTimer
import threading
import serial.tools.list_ports
import csv

# Find the port to which the Arduino is connected
def cautare_port():
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        if "CH340" in port.description:
            return port.device
    return None

# Function to read data from Arduino
def citeste_date(port, data_list):
    buffer = ""
    with serial.Serial(port, 115200, timeout=1) as ser:
        while True:
            try:
                buffer += ser.read(ser.in_waiting or 1024).decode('utf-8')
                if '\n' in buffer:
                    lines = buffer.split('\n')
                    for line in lines[:-1]:
                        if line.strip():
                            try:
                                numbers = [float(x) for x in line.split()]
                                data_list.append(numbers)
                                print(f"Data received: {numbers}")  # Debugging: Print received data
                            except ValueError as e:
                                print(f"Error converting data to float: {e}")
                    buffer = lines[-1]
            except Exception as e:
                print(f"Error reading data: {e}")

class Raw(QMainWindow):
    def __init__(self, main_window_reference):
        super().__init__()
        self.data_list = []
        self.saving_data = False

        # Start data reading thread
        port = cautare_port()
        if port:
            self.thread = threading.Thread(target=citeste_date, args=(port, self.data_list))
            self.thread.daemon = True
            self.thread.start()

        # Setează titlul ferestrei
        self.setWindowTitle("Terminal Emulator")

        # Creează butoanele de ieșire și revenire
        self.exit_button = QPushButton("Exit", self)
        self.exit_button.setStyleSheet("background-color: #c0392b; color: white; border-radius: 15px; font-weight: bold;")
        self.exit_button.clicked.connect(self.close)

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

        # Display the data list in the terminal output
        for data in self.data_list:
            # Join the list of numbers into a single string separated by commas and enclosed in square brackets
            data_str = '[{}]'.format(', '.join(map(str, data)))
            self.terminal_output.append(data_str)

    def return_to_main_page(self):
        # Afișează fereastra principală și ascunde fereastra curentă
        self.main_window_reference.show()
        self.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Raw(None)
    window.showFullScreen()
    sys.exit(app.exec_())
