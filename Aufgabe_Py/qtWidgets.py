import sys

from PyQt5.QtCore import (Qt,QDateTime, QLocale)
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
    QDialogButtonBox,
    QTextBrowser,
)
from PyQt5.QtGui import QPalette, QColor, QDoubleValidator
class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

class NumberOnlyLineEdit(QLineEdit):
 def __init__(self, parent=None):
        super().__init__(parent)
        
        validator = QDoubleValidator()
        validator.setDecimals(2)
        validator.setLocale(QLocale(QLocale.German))
        self.setValidator(validator)


class DialogWindow(QDialog):
    def __init__(self, manager):
        super().__init__()
        # self.setWindowTitle("Dialog Window")
        self.manager = manager
        self.setWindowTitle("Bill")
        self.setGeometry(100, 100, 500, 400)

        self.text_browser = QTextBrowser()
        self.text_browser.setHtml(self.generate_bill())

        layout = QVBoxLayout()
        layout.addWidget(self.text_browser)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(button_box)
        self.setLayout(layout)
    def generate_bill(self):
        bill_html = f"<h1>Bill for Jörg</h1>"
        bill_html += "<ul>"

        for row in manager.rows:
            bill_html += f"<li>{row.id}: 3$</li>"

        bill_html += "</ul>"
        bill_html += f"<h2>Total Cost: 50$</h2>"
        return bill_html
        
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
        self.date_edit_von.setDateTime(QDateTime.currentDateTime())
        self.date_edit_bis = QDateEdit(calendarPopup=True)
        self.date_edit_bis.setDateTime(QDateTime.currentDateTime())
        self.line_edit_preis = NumberOnlyLineEdit()
        self.line_edit_preis.setText(str(self.id))
        
        layout = QHBoxLayout()
        layout.addWidget(self.checkbox_use)
        layout.addWidget(self.combobox_art)
        layout.addWidget(self.date_edit_von)
        layout.addWidget(self.date_edit_bis)
        layout.addWidget(self.line_edit_preis)
        self.setLayout(layout)

    def handle_checkbox(self, state):
        # print("handle_checkbox")
        if state == Qt.CheckState.Checked:
            self.manager.add_row()
        else:
            # print("remove row " + str(self.id))
            self.manager.remove_row(self.id)
            
class RowManager(QWidget):
    def __init__(self):
        super().__init__()
        self.id = 0
        self.rows = []
        self.rows_layout = QVBoxLayout()
        if len(self.rows) == 0: 
            self.add_row()
            
        self.setLayout(self.rows_layout)
    def add_row(self):
        id = self.id
        row = RowWidget(id,self)
        self.id += 1
        self.rows.append(row)
        self.rows_layout.addWidget(row)
    def remove_row(self, id):
        for row in self.rows:
            if row.id == id:
                removedRow = row
                self.rows.remove(removedRow)
                removedRow.setParent(None)
                removedRow.deleteLater()

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
        dialog = DialogWindow(manager)
        if dialog.exec_() == QDialog.Accepted:
            print("Dialog accepted")
        else:
            print("Dialog rejected")

app = QApplication(sys.argv)
manager = RowManager()
window = MainWindow(manager)
window.show()

sys.exit(app.exec())