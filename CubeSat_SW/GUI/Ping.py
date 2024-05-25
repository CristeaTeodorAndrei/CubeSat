import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt, QTimer
import serial.tools.list_ports
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from datetime import datetime, timedelta
import logging
import time

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to find the port to which the Arduino is connected
def cautare_port():
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        if "CH340" in port.description:
            return port.device
    return None

class Ping(QMainWindow):
    def __init__(self, main_window_reference):
        super().__init__()
        self.start_time = datetime.now()  

        self.setWindowTitle("Charts Page")
        self.setup_ui()
        self.main_window_reference = main_window_reference

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_chart)
        self.timer.start(100)  # Update the chart every 100 ms

        self.serial_data_available = False
        self.impulse_times = []
        self.last_impulse_time = self.start_time

        self.impulse_interval = timedelta(seconds=5)  # 5 seconds between each impulse

        # Start serial communication
        self.serial_thread = threading.Thread(target=self.read_serial_data)
        self.serial_thread.daemon = True
        self.serial_thread.start()

    def setup_ui(self):
        self.exit_button = QPushButton("Exit", self)
        self.exit_button.setStyleSheet("background-color: #c0392b; color: white; border-radius: 15px; font-weight: bold;")
        self.exit_button.clicked.connect(self.close)

        self.back_button = QPushButton("Main Page", self)
        self.back_button.setStyleSheet("background-color: #c0392b; color: white; border-radius: 15px; font-weight: bold;")
        self.back_button.clicked.connect(self.return_to_main_page)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.exit_button)

        main_layout = QVBoxLayout()
        chart_layout = QVBoxLayout()
        self.add_chart(chart_layout)

        main_layout.addLayout(chart_layout)
        main_layout.addLayout(button_layout)

        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #1E1E1E;") 
        central_widget.setLayout(main_layout)

        self.setCentralWidget(central_widget)

        self.back_button.setFixedSize(100, 50)
        self.exit_button.setFixedSize(100, 50)
        button_layout.setAlignment(self.back_button, Qt.AlignLeft)
        button_layout.setAlignment(self.exit_button, Qt.AlignRight)

        self.showFullScreen()

    def add_chart(self, layout):
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.ax.set_facecolor('#1E1E1E')
        self.fig.patch.set_facecolor('#1E1E1E')

        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')

        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.spines['top'].set_color('white')
        self.ax.spines['right'].set_color('white')

        self.canvas = FigureCanvas(self.fig)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout.addWidget(self.canvas)

    def update_chart(self):
        current_time = datetime.now()
        elapsed_time = (current_time - self.start_time).total_seconds()
        self.time = np.arange(0, elapsed_time + 0.1, 0.1)

        self.signal = np.zeros_like(self.time)

        # Update the signal array based on the impulse times
        for impulse_time in self.impulse_times:
            index = int((impulse_time - self.start_time).total_seconds() * 10)
            if index < len(self.signal):
                self.signal[index] = 1

        self.ax.clear()
        self.ax.plot(self.time, self.signal, color='green', linewidth=3.0)  # Thicker green line
        self.ax.set_ylim(-0.1, 1.1)
        self.ax.set_title("Ping Test", color='white', fontsize=30, pad=20, fontweight='bold')
        self.ax.set_xlabel("Time (s)", color='white', fontsize=16, fontweight='bold')
        self.ax.set_ylabel("Value (num)", color='white', fontsize=16, fontweight='bold')
        self.ax.grid(color='black', linewidth=0.5)

        self.canvas.draw()

    def return_to_main_page(self):
        self.main_window_reference.show()
        self.hide()

    def read_serial_data(self):
        while True:
            port_device = cautare_port()
            if port_device:
                try:
                    with serial.Serial(port_device, 115200, timeout=1) as ser:
                        logging.info(f"Connected to port: {port_device}")
                        while True:
                            line = ser.readline().decode().strip()
                            if line:
                                self.serial_data_available = True
                                current_time = datetime.now()
                                if current_time - self.last_impulse_time >= self.impulse_interval:
                                    self.impulse_times.append(current_time)
                                    self.last_impulse_time = current_time
                                    logging.info("Impulse detected and added.")
                except serial.SerialException as e:
                    logging.warning(f"Serial exception: {e}")
                    self.serial_data_available = False
                except Exception as e:
                    logging.error(f"Unexpected error: {e}")
                    self.serial_data_available = False
            else:
                logging.info("No port found, retrying in 5 seconds...")

if __name__ == "__main__":
    app = QApplication([])
    window = Ping(None)
    app.exec_()
