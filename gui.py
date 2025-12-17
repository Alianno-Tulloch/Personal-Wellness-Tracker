import sys

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt

app = QApplication([])

window = QWidget()
window.show()

app.exec()


"""
For now, only start working on the "Entry input" and CSV parts of the GUI.
The graphing/visualizing stuff will be added on later, don't worry about
the code/implementation for that right now
"""