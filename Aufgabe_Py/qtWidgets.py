import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QDialogButtonBox

)
from PyQt5.QtGui import QPalette, QColor
class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

class RowWidget(QWidget):
    def __init__(self, id, parent=None):
        super().__init__(parent)
        self.id = id
        self.checkbox_use = QCheckBox()
        self.checkbox_use.billrow = 1
        self.checkbox_use.stateChanged.connect(self.handle_checkbox)
        self.combobox_art = QComboBox()
        self.combobox_art.addItems(["Foo","Baar"])
        self.date_edit_von = QDateEdit(calendarPopup=True)
        self.date_edit_bis = QDateEdit(calendarPopup=True)
        self.line_edit_preis = QLineEdit()
        
        layout = QHBoxLayout()
        layout.addWidget(self.checkbox_use)
        layout.addWidget(self.combobox_art)
        layout.addWidget(self.date_edit_von)
        layout.addWidget(self.date_edit_bis)
        layout.addWidget(self.line_edit_preis)
        self.setLayout(layout)
    
    def remove_self(self):
        self.setParent(None)
        self.deleteLater()
    def handle_checkbox(self, state):
        if state == Qt.CheckState.Checked:
            manager.add_row()
            
class RowManager(QWidget):
    def __init__(self):
        super().__init__()
        self.rows = {}
        self.rows_layout = QVBoxLayout()
        if len(self.rows) == 0: 
            self.add_row()
            
        self.setLayout(self.rows_layout)
    def add_row(self):
        id = len(self.rows)
        row = RowWidget(id)
        self.rows[id] = row
        self.rows_layout.addWidget(row)
        print("adding a row")    

class MainWindow(QMainWindow):

    # def checkboxClicked(self,):
    #     check1 = self.sender()
    #     if check1.isChecked() == True:        
    #         print("checkbox clicked and checked " + str( check1.billrow) + " row ")
    #     else: 
    #         print("uncheckbox checkbox on row " + str(check1.billrow) + " ")
    def close(self):
        sys.exit()
    def setButtons(self,layout):
        buttonGroup = QHBoxLayout()
        buttonGroup.addStretch()
        buttonShowBill = QPushButton('Rechnung Anzeigen', self)
        buttonShowBill.setFixedWidth(120)
        buttonClose = QPushButton('Beenden',self)
        buttonClose.setFixedWidth(70)
        buttonClose.clicked.connect(self.close)
        buttonGroup.addWidget(buttonShowBill)
        buttonGroup.addWidget(buttonClose)
        layout.addLayout(buttonGroup)

    def __init__(self,manager, parent = None):
        super().__init__()

        self.setWindowTitle("Widgets App")
        rowManager = manager
        layout = QVBoxLayout()
        layout.addWidget(rowManager)
        layout.addStretch()
        self.setButtons(layout)
        widget = QWidget() # Color('green')
        widget.setLayout(layout)
        self.setMinimumSize(800,200)
        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(widget)


app = QApplication(sys.argv)
manager = RowManager()
window = MainWindow(manager)
window.show()

sys.exit(app.exec())