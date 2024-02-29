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
    QScrollArea,
    QErrorMessage,
)
from PyQt5.QtGui import QFocusEvent, QKeyEvent, QPalette, QColor, QDoubleValidator
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
        
        # validator = QDoubleValidator()
        # validator.setDecimals(2)
        # validator.setLocale(QLocale(QLocale.German))
        # self.setValidator(validator)
        # self.textChanged.connect(self.handle_text_changed)
        self.error_message = QErrorMessage()
            
    def keyPressEvent(self, event: QKeyEvent|None) -> None:
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            print("enter key")
            self.handle_text_changed()
        else:
            return super().keyPressEvent(event)

    def focusOutEvent(self, a0: QFocusEvent | None) -> None:
        self.handle_text_changed()
        return super().focusOutEvent(a0)
    
    def handle_text_changed(self):
        if self.text().strip() == "":
            self.setText("0.00") 
        try:
            value = float(self.text())
            formated_text = "{:.2f}".format(value)
            self.setText(formated_text)
        except ValueError:
            self.clear()
            self.setText("0.00")
            self.error_message.showMessage("Nicht gültige Eingabe")
    
class DialogWindow(QDialog):
    def __init__(self, manager):
        super().__init__()
        # self.setWindowTitle("Dialog Window")
        self.manager = manager
        self.setWindowTitle("Rechnung")
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
        # only those are checked
        self.s_row = [row for row in manager.rows if row.checkbox_use.isChecked()]
        self.total = sum(float(row.line_edit_preis.text()) for row in self.s_row)
        self.total = "{:.2f}".format(self.total)
        bill_html = """
        <h2>Rechnung</h2><hr>
        <table border="0" width="100%">
            <thead>
                <tr>
                    <th align="left">#</th>
                    <th align="left">Art</th>
                    <th align="left">Zeitraum</th>
                    <th align="left">Betrag in €</th>
                </tr>
            </thead>
            <tbody>"""
        
        for index,row in enumerate(self.s_row, start=1):
            # if row.checkbox_use.isChecked():
            zeitraum = row.date_edit_von.date().toString("dd.MM.yyyy")
            zeitraum += " - "
            zeitraum += row.date_edit_bis.date().toString("dd.MM.yyyy")
            bill_html += f"""
            <tr>
                <td>{index}</td>
                <td>{row.combobox_art.currentText()}</td>
                <td>{zeitraum}</td>
                <td>{row.line_edit_preis.text()}</td>
            </tr>"""

        bill_html += """
        </tbody></table><hr>"""
        bill_html += f"""
        <h2>Gesamtbetrag (Eruo): {self.total}</h2>"""
        return bill_html
        
class RowWidget(QWidget):
    def __init__(self, id,foo_manager, parent=None):
        super().__init__(parent)
        self.manager = foo_manager
        self.id = id
        
        self.checkbox_use = QCheckBox()
        self.checkbox_use.setFixedWidth(15)
        # self.checkbox_use.billrow = 1
        
        self.checkbox_use.stateChanged.connect(self.handle_checkbox)
        self.combobox_art = QComboBox()
        self.combobox_art.setFixedWidth(140)
        self.combobox_art.addItems(["Halbpension","Vollpension","Spezialangebot"])
        
        self.date_edit_von = QDateEdit(calendarPopup=True)
        self.date_edit_von.setFixedWidth(150)
        self.date_edit_von.setDateTime(QDateTime.currentDateTime())
        self.date_edit_von.dateTimeChanged.connect(self.handle_date_time_changed_von)
        
        self.date_edit_bis = QDateEdit(calendarPopup=True)
        self.date_edit_bis.setFixedWidth(150)
        self.date_edit_bis.setDateTime(QDateTime.currentDateTime().addDays(1))
        self.date_edit_bis.dateTimeChanged.connect(self.handle_date_time_changed_bis)
        
        self.line_edit_preis = NumberOnlyLineEdit()
        self.line_edit_preis.setFixedWidth(250)
        self.line_edit_preis.setText("0.00")
        
        layout = QHBoxLayout()
        layout.addWidget(self.checkbox_use)
        layout.addStretch()
        layout.addWidget(self.combobox_art)
        layout.addWidget(self.date_edit_von)
        layout.addWidget(self.date_edit_bis)
        layout.addWidget(self.line_edit_preis)
        self.set_visible(False)
        self.setLayout(layout)
        
    def set_visible(self,visible):
        self.combobox_art.setVisible(visible)
        self.date_edit_von.setVisible(visible)
        self.date_edit_bis.setVisible(visible)
        self.line_edit_preis.setVisible(visible)
        
    def handle_date_time_changed_bis(self):
        # if vom > bis set vom to bis
        if self.date_edit_von.dateTime() > self.date_edit_bis.dateTime():
            self.date_edit_von.setDateTime(self.date_edit_bis.dateTime())
            self.date_edit_von.setDateTime(self.date_edit_von.dateTime().addDays(-1))
            
    def handle_date_time_changed_von(self):
        # if bis > vom set bis to vom
        if self.date_edit_bis.dateTime() < self.date_edit_von.dateTime():
            self.date_edit_bis.setDateTime(self.date_edit_von.dateTime())
            self.date_edit_bis.setDateTime(self.date_edit_bis.dateTime().addDays(1))    
            
    def handle_checkbox(self, state):
        # print("handle_checkbox")
        if state == Qt.CheckState.Checked:
            self.set_visible(True)
            self.manager.add_row()
        else:
            # print("remove row " + str(self.id))
            self.manager.remove_row(self.id)

class RowWidgetHeader(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.empty_box = QLabel("")
        self.empty_box.setFixedWidth(15)
        self.art_label = QLabel("Art")
        self.art_label.setFixedWidth(140)
        self.von_label = QLabel("Vom")
        self.von_label.setFixedWidth(150) 
        self.bis_label = QLabel("Bis")
        self.bis_label.setFixedWidth(150)
        self.preis_label = QLabel("Preis in Euro")
        self.preis_label.setFixedWidth(250)
        layout = QHBoxLayout()
        layout.addWidget(self.empty_box)
        layout.addStretch()
        layout.addWidget(self.art_label)
        layout.addWidget(self.von_label)
        layout.addWidget(self.bis_label)
        layout.addWidget(self.preis_label)
        self.setLayout(layout)
         
class RowManager(QWidget):
    def __init__(self):
        super().__init__()
        self.id = 0
        self.rows = []
        self.rows_layout = QVBoxLayout()
        header = RowWidgetHeader(self)
        self.rows_layout.addWidget(header)
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
        buttonShowBill = QPushButton('Rechnung anzeigen', self)
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

        self.setWindowTitle("Buchungsabrechnung")
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.rowManager = manager
        layout = QVBoxLayout()
        layout.addWidget(self.rowManager)
        layout.addStretch()
        self.setButtons(layout)
        widget = QWidget() # Color('green')
        widget.setLayout(layout)
        self.setFixedSize(800,600)
        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.scroll.setWidget(widget)
        self.setCentralWidget(self.scroll)
    def show_dialog(self):
        # print("getting the row out of the manager shit " + str(len(self.rowManager.rows)))
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