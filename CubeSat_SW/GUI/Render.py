import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
import threading
import serial.tools.list_ports
from vispy import scene

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
                            except ValueError as e:
                                print(f"Error converting data to float: {e}")
                    buffer = lines[-1]
            except Exception as e:
                print(f"Error reading data: {e}")

class Render(QMainWindow):
    def __init__(self, main_window_reference):
        super().__init__()
        self.data_list = []

        # Start data reading thread
        port = cautare_port()
        if port:
            self.thread = threading.Thread(target=citeste_date, args=(port, self.data_list))
            self.thread.daemon = True
            self.thread.start()

        # Set the title of the window
        self.setWindowTitle("3D Cube Visualization")

        # Create exit and back buttons
        self.exit_button = QPushButton("Exit", self)
        self.exit_button.setFixedSize(100, 50)
        self.exit_button.setStyleSheet("background-color: #c0392b; color: white; border-radius: 15px; font-weight: bold;")
        self.exit_button.clicked.connect(self.close)

        self.back_button = QPushButton("Main Page", self)
        self.back_button.setFixedSize(100, 50)
        self.back_button.setStyleSheet("background-color: #c0392b; color: white; border-radius: 15px; font-weight: bold;")
        self.back_button.clicked.connect(self.return_to_main_page)

        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button)
        button_layout.addStretch()
        button_layout.addWidget(self.exit_button)

        # Reference to the main window
        self.main_window_reference = main_window_reference

        # Setup 3D cube visualization
        self.canvas = scene.SceneCanvas(keys='interactive', show=True)
        self.view = self.canvas.central_widget.add_view()
        self.view.camera = 'turntable'
        self.cube = scene.visuals.Box(width=1, height=1, depth=1, color='white', edge_color='black')
        self.view.add(self.cube)

        self.rotation_timer = QTimer(self)
        self.rotation_timer.timeout.connect(self.update_cube_rotation)
        self.rotation_timer.start(1)  # Update every 10 milliseconds for faster updates

        # Embed Vispy canvas into PyQt5 layout
        layout = QVBoxLayout()
        layout.addWidget(self.canvas.native)
        layout.addLayout(button_layout)

        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #1E1E1E;")
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Set window to fullscreen
        self.showFullScreen()

    def update_cube_rotation(self):
        if self.data_list:
            last_data = self.data_list[-1]
            if len(last_data) >= 11:
                x, y, z = last_data[8:11]
                self.cube.transform = scene.transforms.MatrixTransform()
                self.cube.transform.rotate(x, (1, 0, 0))
                self.cube.transform.rotate(y, (0, 1, 0))
                self.cube.transform.rotate(z, (0, 0, 1))
                self.canvas.update()

    def return_to_main_page(self):
        # Show the main window and hide the current window
        self.main_window_reference.show()
        self.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Raw(None)
    window.showFullScreen()
    sys.exit(app.exec_())
