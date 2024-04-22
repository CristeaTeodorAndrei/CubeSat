from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt, QTimer
import serial.tools.list_ports
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from datetime import datetime, timedelta  # Importăm timedelta aici
import serial

# Importarea functiilor din fisierul Get_Data.py
from Get_Data import cautare_port

class Ping(QMainWindow):
    def __init__(self, main_window_reference):
        super().__init__()
        self.start_time = datetime.now()  

        self.setWindowTitle("Charts Page")

        self.exit_button = QPushButton("Exit", self)
        self.exit_button.setStyleSheet("background-color: #c0392b; color: white; border-radius: 15px; font-weight: bold;")
        self.exit_button.clicked.connect(self.close)

        self.back_button = QPushButton("Main Page", self)
        self.back_button.setStyleSheet("background-color: #c0392b; color: white; border-radius: 15px; font-weight: bold;")
        self.back_button.clicked.connect(self.return_to_main_page)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.exit_button)

        self.main_window_reference = main_window_reference

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

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_chart)
        self.timer.start(500)

        self.serial_data_available = False

        # Lista timpilor la care apar impulsurile
        self.impulse_times = []

        # Apelarea functiei cautare_port din Get_Data.py pentru a gasi portul
        self.port = cautare_port()
        if self.port:
            # Inceperea unui fir separat pentru citirea datelor de la Arduino
            self.serial_thread = threading.Thread(target=self.citeste_date_thread)
            self.serial_thread.daemon = True
            self.serial_thread.start()
        else:
            print("Nema.")

    def add_chart(self, layout):
        self.fig, self.ax = plt.subplots(figsize=(8, 6))  

        self.ax.set_facecolor('#1E1E1E')  

        self.fig.patch.set_facecolor('#1E1E1E')

        for line in self.ax.get_lines():
            line.set_color('white')

        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')

        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.spines['top'].set_color('white')
        self.ax.spines['right'].set_color('white')

        elapsed_time = (datetime.now() - self.start_time).total_seconds()
        self.time = np.arange(0, elapsed_time + 1, 0.1)  

        self.signal = np.zeros_like(self.time)  

        self.ax.plot(self.time, self.signal, color='green')  

        self.ax.set_ylim(0, 2)

        self.ax.set_title("Ping Test", color='white', fontsize=30, pad=20, fontweight='bold')

        self.ax.set_xlabel("Time (s)", color='white', fontsize=16, fontweight='bold')

        self.ax.set_ylabel("Value (num)", color='white', fontsize=16, fontweight='bold')

        self.ax.grid(color='black', linewidth=0.5)

        self.canvas = FigureCanvas(self.fig)

        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        layout.addWidget(self.canvas)

    def update_chart(self):
        current_time = datetime.now()
        elapsed_time = (current_time - self.start_time).total_seconds()
        self.time = np.arange(0, elapsed_time + 1, 0.1)

        # Reset the signal to zeros at each update
        self.signal = np.zeros_like(self.time)  

        # Calculate the time since the last impulse
        time_since_last_impulse = (current_time - self.impulse_times[-1] if self.impulse_times else timedelta(seconds=2)).total_seconds()

        if self.serial_data_available and time_since_last_impulse >= 2:  # Send impulse every 2 seconds
            # Add the current time to the list of impulse times
            self.impulse_times.append(current_time)

        # Update the signal array based on the impulse times
        for impulse_time in self.impulse_times:
            index = int((impulse_time - self.start_time).total_seconds() * 10)
            if index < len(self.signal):
                self.signal[index] = 1

        self.ax.clear()
        self.ax.plot(self.time, self.signal, color='green')
        self.ax.set_ylim(0, 2)
        self.ax.set_title("Ping Test", color='white', fontsize=30, pad=20, fontweight='bold')
        self.ax.set_xlabel("Time (s)", color='white', fontsize=16, fontweight='bold')
        self.ax.set_ylabel("Value (num)", color='white', fontsize=16, fontweight='bold')
        self.ax.grid(color='black', linewidth=0.5)

        self.canvas.draw()

    def return_to_main_page(self):
        self.main_window_reference.show()
        self.hide()

    def citeste_date_thread(self):
        with serial.Serial(self.port, 9600, timeout=1) as ser:
            while True:
                line = ser.readline().decode().strip()
                if line:  # Verifica daca exista date primite
                    self.serial_data_available = True
                else:
                    self.serial_data_available = False

if __name__ == "__main__":
    app = QApplication([])
    window = Ping(None)

    app.exec_()
