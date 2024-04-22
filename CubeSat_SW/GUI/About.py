from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QSizePolicy
from PyQt5.QtCore import Qt  # Adaugă importul pentru Qt

class About(QMainWindow):
    def __init__(self, main_window_reference):
        super().__init__()

        # Setează titlul ferestrei
        self.setWindowTitle("About")

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

        # Creează un QLabel pentru textul "Student: Cristea Teodor - Andrei"
        student_label = QLabel("Student: Cristea Teodor - Andrei", self)
        student_label.setAlignment(Qt.AlignCenter)
        student_label.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")

        project_label = QLabel("Project: CubeSAT", self)
        project_label.setAlignment(Qt.AlignCenter)
        project_label.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")

        version_label = QLabel("Version: 1.0.0", self)
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")

        # Adaugă QLabel-urile la layout-ul principal
        main_layout.addStretch()
        main_layout.addWidget(project_label)
        main_layout.addWidget(version_label)
        main_layout.addWidget(student_label)
        main_layout.addStretch()

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

    def return_to_main_page(self):
        # Afișează fereastra principală și ascunde fereastra curentă
        self.main_window_reference.show()
        self.hide()

if __name__ == "__main__":
    app = QApplication([])
    window = About(None)
    app.exec_()
