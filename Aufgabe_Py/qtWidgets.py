import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QDialog,
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
        
class DialogWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dialog Window")

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("This is a dialog window"))
        layout.addWidget(button_box)
        self.setLayout(layout)
        
class RowWidget(QWidget):
    def __init__(self, id,foo_manager, parent=None):
        super().__init__(parent)
        self.manager = foo_manager
        self.id = id
        self.checkbox_use = QCheckBox()
        self.checkbox_use.billrow = 1
        self.checkbox_use.stateChanged.connect(self.handle_checkbox)
        self.combobox_art = QComboBox()
        self.combobox_art.addItems(["Foo","Baar"])
        self.date_edit_von = QDateEdit(calendarPopup=True)
        self.date_edit_bis = QDateEdit(calendarPopup=True)
        self.line_edit_preis = QLineEdit()
        self.line_edit_preis.setText(str(self.id))
        
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
            self.manager.add_row()
        else:
            self.manager.remove_row(self.id)
            
class RowManager(QWidget):
    def __init__(self):
        super().__init__()
        self.rows = []
        self.rows_layout = QVBoxLayout()
        if len(self.rows) == 0: 
            self.add_row()
            
        self.setLayout(self.rows_layout)
    def add_row(self):
        id = len(self.rows)
        row = RowWidget(id,self)
        self.rows.append(row)
        self.rows_layout.addWidget(row)
        print("adding a row")    
    def remove_row(self, id):
        if len(self.rows) > 1:
            row = self.rows.pop()
            row.setParent(None)
            row.deleteLater()

class MainWindow(QMainWindow):

    def close(self):
        sys.exit()
    def setButtons(self,layout):
        buttonGroup = QHBoxLayout()
        buttonGroup.addStretch()
        buttonShowBill = QPushButton('Rechnung Anzeigen', self)
        buttonShowBill.setFixedWidth(120)
        buttonShowBill.clicked.connect(self.show_dialog)
        buttonClose = QPushButton('Beenden',self)
        buttonClose.setFixedWidth(70)
        buttonClose.clicked.connect(self.close)
        buttonGroup.addWidget(buttonShowBill)
        buttonGroup.addWidget(buttonClose)
        layout.addLayout(buttonGroup)

    def __init__(self,manager, parent = None):
        super().__init__()

        self.setWindowTitle("Widgets App")
        self.rowManager = manager
        layout = QVBoxLayout()
        layout.addWidget(self.rowManager)
        layout.addStretch()
        self.setButtons(layout)
        widget = QWidget() # Color('green')
        widget.setLayout(layout)
        self.setMinimumSize(800,300)
        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(widget)
    def show_dialog(self):
        print("getting the row out of the manager shit " + str(len(self.rowManager.rows)))
        dialog = DialogWindow()
        if dialog.exec_() == QDialog.Accepted:
            print("Dialog accepted")
        else:
            print("Dialog rejected")

app = QApplication(sys.argv)
manager = RowManager()
window = MainWindow(manager)
window.show()

sys.exit(app.exec())