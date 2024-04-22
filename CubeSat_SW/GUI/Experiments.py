from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt  # Adaugă importul pentru Qt

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

class Experiments(QMainWindow):
    def __init__(self, main_window_reference):
        super().__init__()

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

        # Creează un layout orizontal pentru graficele de pe prima linie
        first_row_layout = QHBoxLayout()

        # Adaugă 3 grafice la layout-ul de pe prima linie
        for i in range(3):
            self.add_chart(first_row_layout, i)

        # Adaugă layout-ul de pe prima linie la layout-ul principal
        main_layout.addLayout(first_row_layout)

        # Creează un layout orizontal pentru graficele de pe a doua linie
        second_row_layout = QHBoxLayout()

        # Adaugă 3 grafice la layout-ul de pe a doua linie
        for i in range(3, 6):
            self.add_chart(second_row_layout, i)

        # Adaugă layout-ul de pe a doua linie la layout-ul principal
        main_layout.addLayout(second_row_layout)

        # Creează un layout orizontal pentru graficele de pe a treia linie
        third_row_layout = QHBoxLayout()

        # Adaugă 3 grafice la layout-ul de pe a treia linie
        for i in range(6, 9):
            self.add_chart(third_row_layout, i)

        # Adaugă layout-ul de pe a treia linie la layout-ul principal
        main_layout.addLayout(third_row_layout)

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

    def add_chart(self, layout, index):
        # Creează o figură Matplotlib (mai mică)
        fig, ax = plt.subplots(figsize=(5, 3))
        plt.subplots_adjust(left=0.15, right=0.85, bottom=0.2, top=0.9)
        # Setează fundalul pentru subplot la culoarea dorită
        ax.set_facecolor('#1E1E1E')  # Setează culoarea fundalului graficului

        # Setează fundalul pentru frame-ul figurii Matplotlib la aceeași culoare ca și subplot-ul
        fig.patch.set_facecolor('#1E1E1E')

        # Setează culoarea tuturor liniilor graficului la alb și le face mai transparente
        for line in ax.get_lines():
            line.set_color('white')
            #line.set_alpha(1)  # Setează transparența liniilor

        # Setează culoarea notițiilor de pe axele x și y la alb
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        # Setează culoarea axelor la alb
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['top'].set_color('white')
        ax.spines['right'].set_color('white')

        # Generează date aleatorii pentru grafic
        x = np.linspace(0, 10, 100)
        y = np.random.rand(100)

        # Desenează graficul
        ax.plot(x, y, color='green')  # Setează culoarea liniilor la verde

        # Afișează o grilă neagră pe grafic
        ax.grid(color='black', linewidth=0.5)

        # Adaugă eticheta pe axa OX
        ax.set_xlabel('Time (s)', color='white')

        # Adaugă eticheta pe axa OY în funcție de indexul graficului
        labels = ['Accel_X (m/s^2)', 'Accel_Y (m/s^2)', 'Accel_Z (m/s^2)', 'Mag_X (mT)', 'Mag_Y (mT)', 'Mag_Z (mT)', 'Temp (C)', 'Load (%)', 'Voltage (V)']
        ax.set_ylabel(labels[index], color='white')

        # Creează un canvas pentru a afișa figura Matplotlib în Qt
        canvas = FigureCanvas(fig)

        # Scalează canvas-ul la dimensiunea dorită (păstrează aspectul)
        canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Ignored)

        # Adaugă canvas-ul la layout
        layout.addWidget(canvas)

    def return_to_main_page(self):
        # Afișează fereastra principală și ascunde fereastra curentă
        self.main_window_reference.show()
        self.hide()

if __name__ == "__main__":
    app = QApplication([])
    window = Experiments(None)
    app.exec_()
