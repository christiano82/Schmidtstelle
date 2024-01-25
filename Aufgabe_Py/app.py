# from PyQt5.QtWidgets import QApplication, QLabel

# app = QApplication([])
# label = QLabel('Hello Schmiddi')
# label.show()
# app.exec_()
# from PyQt5.QtWidgets import *
# app = QApplication([])
# app.setStyle('Fusion')
# window = QWidget()
# layout = QVBoxLayout()
# buttonTop = QPushButton('Top Schmiddi')

# def on_button_clicked():
#     alert = QMessageBox()
#     alert.setText('Schmiddi man der Button ist geklickt')
#     alert.exec()

# buttonTop.clicked.connect(on_button_clicked)
# layout.addWidget(buttonTop)
# layout.addWidget(QPushButton('Bottom'))
# window.setLayout(layout)
# window.show()
# app.exec()

import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        button = QPushButton("Press Me!")
        button.clicked.connect(self.on_button_clicked)
        self.setFixedSize(QSize(400, 300))
        # Set the central widget of the Window.
        self.setCentralWidget(button)
    def on_button_clicked(self):
        print("Clicked!")

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()