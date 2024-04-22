import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QDateTimeEdit
from PyQt5.QtCore import Qt, QTimer, QDateTime
import datetime  # Importă modulul datetime


from Ping import Ping
from System_Monitor import System_Monitor
from Experiments import Experiments
from About import About

class CubeSATDashboard(QMainWindow):
    def __init__(self):
        super().__init__()

        # Setează titlul ferestrei
        self.setWindowTitle("CubeSAT Dashboard")

        # Setează dimensiunile ferestrei
        self.setGeometry(0, 0, 1920, 1080)

        # Setează fundalul la întuneric
        self.setStyleSheet("background-color: #1E1E1E;")

        # Adaugă titlul
        title_label = QLabel("CubeSAT Dashboard", self)
        title_label.setStyleSheet("color: white; font-size: 40pt; font-weight: bold; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setGeometry(0, 150, 1920, 100)

        # Creează butoanele
        button1 = QPushButton("Ping", self)
        button1.setGeometry(1920//2 - 100, 400, 200, 50)
        button1.setStyleSheet("background-color: #27ae60; color: white; border-radius: 10px; font-weight: bold;")
        button1.clicked.connect(self.show_ping) 

        button2 = QPushButton("System Monitor", self)
        button2.setGeometry(1920//2 - 100, 500, 200, 50)
        button2.setStyleSheet("background-color: #3498db; color: white; border-radius: 10px; font-weight: bold;")
        button2.clicked.connect(self.show_system_monitor) 

        button3 = QPushButton("Measurements", self)
        button3.setGeometry(1920//2 - 100, 600, 200, 50)
        button3.setStyleSheet("background-color: #3498db; color: white; border-radius: 10px; font-weight: bold;")
        button3.clicked.connect(self.show_experiments) 

        button4 = QPushButton("About", self)
        button4.setGeometry(1920//2 - 100, 700, 200, 50)
        button4.setStyleSheet("background-color: #674732; color: white; border-radius: 10px; font-weight: bold;")
        button4.clicked.connect(self.show_about)

        # Creează butonul de ieșire
        exit_button = QPushButton("Exit", self)
        exit_button.setGeometry(1920 - 100, 1080 - 30, 100, 30)
        exit_button.setStyleSheet("background-color: #c0392b; color: white; border-radius: 5px; font-weight: bold;")
        exit_button.clicked.connect(self.close)

        # Adaugă data și ora în timp real în partea stângă jos a ferestrei
        self.date_time_label = QLabel("", self)
        self.date_time_label.setStyleSheet("color: white; font-size: 20pt; font-weight: bold;")
        self.date_time_label.setGeometry(20, 0, 300, 30)

        # Actualizează data și ora în timp real folosind un timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_date_time)
        self.timer.start(1000)  # Actualizează data și ora la fiecare secundă

        # Setează fereastra să fie fullscreen
        self.setWindowState(Qt.WindowFullScreen)

    def update_date_time(self):
        # Obține data și ora curentă de pe laptop
        now = datetime.datetime.now()

        # Formatează data și ora într-un format ușor de citit
        formatted_date_time = now.strftime("%Y-%m-%d %H:%M:%S")

        # Actualizează textul etichetei cu data și ora curentă
        self.date_time_label.setText(formatted_date_time)

    def show_system_monitor(self):  
        # Ascunde fereastra curentă și afișează fereastra System_Monitor
        self.hide()
        self.system_monitor_window = System_Monitor(self)
        self.system_monitor_window.show()
    
    def show_ping(self):  
        # Ascunde fereastra curentă și afișează fereastra System_Monitor
        self.hide()
        self.system_monitor_window = Ping(self)
        self.system_monitor_window.show()

    def show_experiments(self):  
        # Ascunde fereastra curentă și afișează fereastra System_Monitor
        self.hide()
        self.system_monitor_window = Experiments(self)
        self.system_monitor_window.show()

    def show_about(self):  
        # Ascunde fereastra curentă și afișează fereastra System_Monitor
        self.hide()
        self.system_monitor_window = About(self)
        self.system_monitor_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CubeSATDashboard()
    window.showFullScreen()
    sys.exit(app.exec_())
