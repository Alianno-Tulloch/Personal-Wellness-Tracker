import sys

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QLineEdit, QPushButton, QFileDialog, QMessageBox, QMainWindow
)
from PySide6.QtGui import QIntValidator, QDoubleValidator
from PySide6.QtCore import Qt

class InputEntryWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mental Health Tracker App")
        self.resize(600, 600)
        layout = QVBoxLayout()

        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        """
        Date Entry Section
        """
        main_layout.addWidget(QLabel("Enter the Date in the fields below:"))
        date_layout = QHBoxLayout()
        self.date_number_label = QLabel("Day Number")
        self.date_number = QLineEdit()
        self.date_month_label = QLabel("Month")
        self.date_month = QComboBox()
        self.date_month.setEditable(True)
        self.date_month.addItems([
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ])
        self.date_year_label = QLabel("Year")
        self.date_year = QLineEdit()
        date_layout.addWidget(self.date_number_label)
        date_layout.addWidget(self.date_number)
        date_layout.addWidget(self.date_month_label)
        date_layout.addWidget(self.date_month)
        date_layout.addWidget(self.date_year_label)
        date_layout.addWidget(self.date_year)
        main_layout.addLayout(date_layout)


        """
        Exercise Entry Section
        """
        # Sets the validator to only accept integers between 0 and 24
        valid_exercise_hours = QIntValidator(0, 24)
        main_layout.addWidget(QLabel("Enter the amount of time you exercised today:"))
        excersize_layout = QHBoxLayout()
        self.exersize_hours_label = QLabel("Hours")
        self.exercise_hours = QLineEdit()
        self.exercise_hours.
        self.exercise_minutes_label = QLabel("Minutes")
        self.exercise_minutes = QLineEdit()


        """
        Sleep Entry Section
        """
        # Sets the validator to only accept integers between 0 and 24
        valid_sleep_hours = QIntValidator(0, 24)
        sleep_entry_label = QLabel("Sleep Time:")
        sleep_hours = QLineEdit()
        sleep_minutes = QLineEdit()

        """
        Mood Scale Entry Section
        """
        valid_mood_scale = QDoubleValidator(0.0, 10.0, 1)

        """
        Mood Tags Entry Section
        """

        """
        # Activities Entry Section
        """

        """
        Notes Entry Section
        """

        submit_button = QPushButton("Submit Entry")
        # self.setCentralWidget(button)

    

    def submit_entry(self):
        
        create_daily_entry = {
            "date": self.date_entry.text(),
            "hours_slept": self.hours_slept_entry.text(),
            "exercise_minutes": self.exercise_minutes_entry.text(),
            "mood_scale": self.mood_scale_entry.text(),
            "mood_tags": self.mood_tags_entry.text(),
            "activities": self.activities_entry.text(),
            "notes": self.notes_entry.text(),
        }








app = QApplication([])

window = InputEntryWindow()
window.show()

app.exec()


"""
For now, only start working on the "Entry input" and CSV parts of the GUI.
The graphing/visualizing stuff will be added on later, don't worry about
the code/implementation for that right now
"""