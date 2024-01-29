import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout,QHBoxLayout, QWidget, QPushButton, QLineEdit, QLabel, QCheckBox
from PyQt5.QtCore import Qt


class RowWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.label = QLabel('Label:')
        self.line_edit = QLineEdit()
        self.checkbox = QCheckBox('Add new row')
        self.checkbox.stateChanged.connect(self.handle_checkbox)
        self.button = QPushButton('Remove')
        self.button.clicked.connect(self.remove_self)
        
        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.line_edit)
        layout.addWidget(self.checkbox)
        layout.addWidget(self.button)
        
        self.setLayout(layout)
    
    def remove_self(self):
        self.setParent(None)
        self.deleteLater()
    
    def handle_checkbox(self, state):
        if state == Qt.CheckState.Checked:
            manager.add_row()
        else:
            manager.remove_row()


class RowManager(QWidget):
    def __init__(self):
        super().__init__()
        
        self.rows = {}
        self.rows_layout = QVBoxLayout()
        
        self.add_button = QPushButton('Add Row')
        self.add_button.clicked.connect(self.add_row)
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(self.rows_layout)
        main_layout.addWidget(self.add_button)
        
        self.setLayout(main_layout)
    
    def add_row(self):
        row = RowWidget()
        self.rows_layout.addWidget(row)
    def remove_row(self):
        print("remove row")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    manager = RowManager()
    manager.show()
    sys.exit(app.exec_())
