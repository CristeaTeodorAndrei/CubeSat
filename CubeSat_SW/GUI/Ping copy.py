from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt, QTimer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from datetime import datetime
from Get_Data import *
class Ping(QMainWindow):
    def __init__(self, main_window_reference):
        super().__init__()
        self.start_time = datetime.now()  # Memorează momentul deschiderii ferestrei

        # Setează titlul ferestrei
        self.setWindowTitle("Charts Page")

        # Creează butoanele de ieșire și revenire
        self.exit_button = QPushButton("Exit", self)
        self.exit_button.setStyleSheet("background-color: #c0392b; color: white; border-radius: 15px; font-weight: bold;")
        self.exit_button.clicked.connect(self.close)

        self.back_button = QPushButton("Main Page", self)
        self.back_button.setStyleSheet("background-color: #c0392b; color: white; border-radius: 15px; font-weight: bold;")
        self.back_button.clicked.connect(self.return_to_main_page)

        # Creează un layout orizontal pentru butoanele de revenire și ieșire
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.exit_button)

        # Referința către fereastra principală
        self.main_window_reference = main_window_reference

        # Creează un layout principal de tip QVBoxLayout
        main_layout = QVBoxLayout()

        # Creează un layout pentru grafic
        chart_layout = QVBoxLayout()

        # Adaugă un singur grafic la layout-ul de grafic
        self.add_chart(chart_layout)

        # Adaugă layout-ul de grafic la layout-ul principal
        main_layout.addLayout(chart_layout)

        # Adaugă layout-ul butoanelor la layout-ul principal
        main_layout.addLayout(button_layout)

        # Creează un widget central pentru a avea fundalul dorit
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #1E1E1E;")  # Setează culoarea fundalului widget-ului central
        central_widget.setLayout(main_layout)

        # Setează widget-ul central al ferestrei
        self.setCentralWidget(central_widget)

        # Face butoanele mai groase și le plasează în stânga și în dreapta maxim
        self.back_button.setFixedSize(100, 50)
        self.exit_button.setFixedSize(100, 50)
        button_layout.setAlignment(self.back_button, Qt.AlignLeft)
        button_layout.setAlignment(self.exit_button, Qt.AlignRight)

        # Afișează fereastra full screen după ce se inițiază toate componentele
        self.showFullScreen()

        # Setează un timer pentru actualizarea graficului la fiecare 100 ms
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_chart)
        self.timer.start(100)

    def add_chart(self, layout):
        # Creează o figură Matplotlib
        self.fig, self.ax = plt.subplots(figsize=(8, 6))  # Ajustează dimensiunea figsize

        # Setează fundalul pentru subplot la culoarea dorită
        self.ax.set_facecolor('#1E1E1E')  # Setează culoarea fundalului graficului

        # Setează fundalul pentru frame-ul figurii Matplotlib la aceeași culoare ca și subplot-ul
        self.fig.patch.set_facecolor('#1E1E1E')

        # Setează culoarea tuturor liniilor graficului la alb
        for line in self.ax.get_lines():
            line.set_color('white')

        # Setează culoarea notițiilor de pe axele x și y la alb
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')

        # Setează culoarea axelor la alb
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.spines['top'].set_color('white')
        self.ax.spines['right'].set_color('white')

        # Generează date pentru axa timpului în funcție de cât de mult timp a fost deschisă fereastra
        elapsed_time = (datetime.now() - self.start_time).total_seconds()
        self.time = np.arange(0, elapsed_time + 1, 0.1)  # Intervalul de timp consideră timpul scurs de la deschiderea ferestrei

        # Generează semnalul
        self.signal = np.zeros_like(self.time)  # Inițializează semnalul cu valori 0
        self.signal[np.arange(0, len(self.time), int(5/0.1))] = 1  # Setează impulsurile Dirac la fiecare 5 secunde

        # Desenează graficul
        self.ax.plot(self.time, self.signal, color='green')  # Setează culoarea liniilor la verde

        # Setează limitele axei OY la 0 și 2
        self.ax.set_ylim(0, 2)

        # Setează titlul graficului
        self.ax.set_title("Ping Test", color='white', fontsize=30, pad=20, fontweight='bold')

        # Setează denumirea pe axa Ox
        self.ax.set_xlabel("Time (s)", color='white', fontsize=16, fontweight='bold')

        # Setează denumirea pe axa Oy
        self.ax.set_ylabel("Value (num)", color='white', fontsize=16, fontweight='bold')

        # Afișează o grilă neagră pe grafic
        self.ax.grid(color='black', linewidth=0.5)

        # Creează un canvas pentru a afișa figura Matplotlib în Qt
        self.canvas = FigureCanvas(self.fig)

        # Scalează canvas-ul la dimensiunea dorită (păstrează aspectul)
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Adaugă canvas-ul la layout
        layout.addWidget(self.canvas)

    def update_chart(self):
        # Actualizează intervalul de timp și semnalul
        elapsed_time = (datetime.now() - self.start_time).total_seconds()
        self.time = np.arange(0, elapsed_time + 1, 0.1)
        
        if serial_thread():
            self.signal = np.zeros_like(self.time)
            self.signal[np.arange(0, len(self.time), int(5/0.1))] = 1
        else:
            self.signal = np.full_like(self.time, 2)
        
            
        # Actualizează datele graficului
        self.ax.clear()
        self.ax.plot(self.time, self.signal, color='green')
        self.ax.set_ylim(0, 2)
        self.ax.set_title("Ping Test", color='white', fontsize=30, pad=20, fontweight='bold')
        self.ax.set_xlabel("Time (s)", color='white', fontsize=16, fontweight='bold')
        self.ax.set_ylabel("Value (num)", color='white', fontsize=16, fontweight='bold')
        self.ax.grid(color='black', linewidth=0.5)

        # Redesenează canvas-ul
        self.canvas.draw()

    def return_to_main_page(self):
        # Afișează fereastra principală și ascunde fereastra curentă
        self.main_window_reference.show()
        self.hide()

if __name__ == "__main__":
    app = QApplication([])
    window = Ping(None)
    app.exec_()
