import sys
from data_validation import create_daily_entry

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
        Sleep Entry Section
        """
        # Sets the validator to only accept integers between 0 and 24
        valid_sleep_hours = QIntValidator(0, 24)
        valid_sleep_minutes = QIntValidator(0, 59)

        # Adds the sleep entry widgets to the layout
        main_layout.addWidget(QLabel("Enter the amount of time you slept:"))

        # Layout for sleep entry
        sleep_layout = QHBoxLayout()

        # Hours and minutes input fields with labels
        self.sleep_hours_label = QLabel("Hours")
        self.sleep_hours = QLineEdit()
        self.sleep_hours.setValidator(valid_sleep_hours)

        self.sleep_minutes_label = QLabel("Minutes")
        self.sleep_minutes = QLineEdit()
        self.sleep_minutes.setValidator(valid_sleep_minutes)

        # Add widgets to the layout
        sleep_layout.addWidget(self.sleep_hours_label)
        sleep_layout.addWidget(self.sleep_hours)
        sleep_layout.addWidget(self.sleep_minutes_label)
        sleep_layout.addWidget(self.sleep_minutes)
        main_layout.addLayout(sleep_layout)


        """
        Exercise Entry Section
        """
        # Sets the validator to only accept integers between 0 and 24
        valid_exercise_hours = QIntValidator(0, 24)
        valid_exercise_minutes = QIntValidator(0, 59)

        # Adds the exercise entry widgets to the layout
        main_layout.addWidget(QLabel("Enter the amount of time you exercised today:"))
        excersize_layout = QHBoxLayout()

        # Hours and minutes input fields with labels
        self.exersize_hours_label = QLabel("Hours")
        self.exercise_hours = QLineEdit()
        self.exercise_hours.setValidator(valid_exercise_hours)

        self.exercise_minutes_label = QLabel("Minutes")
        self.exercise_minutes = QLineEdit()
        self.exercise_minutes.setValidator(valid_exercise_minutes)

        # Add widgets to the layout
        excersize_layout.addWidget(self.exersize_hours_label)
        excersize_layout.addWidget(self.exercise_hours)
        excersize_layout.addWidget(self.exercise_minutes_label)
        excersize_layout.addWidget(self.exercise_minutes)
        main_layout.addLayout(excersize_layout)


        """
        Mood Scale Entry Section
        """
        main_layout.addWidget(QLabel("Mood scale (0.0 to 10.0):"))
        valid_mood_scale = QDoubleValidator(0.0, 10.0, 1, self)
        self.mood_scale = QLineEdit()
        self.mood_scale.setValidator(valid_mood_scale)
        main_layout.addWidget(self.mood_scale)


        """
        Mood Tags Entry Section
        """


        """
        # Activities Entry Section
        """

        """
        Notes Entry Section
        """

        """
        # Submit Button Section
        """
        main_layout.addWidget(QLabel("Click the button below to submit your entry:"))
        main_layout.addSpacing(10)
        self.submit_button = QPushButton("Submit Entry")
        # Runs the submit_entry function when clicked
        self.submit_button.clicked.connect(self.submit_entry)
        main_layout.addWidget(self.submit_button)

    

    def submit_entry(self):
        # --- Date: day + month + year -> YYYY-MM-DD ---
        day_text = self.date_number.text().strip()
        year_text = self.date_year.text().strip()

        # If the combo box is editable, currentText() captures typed text too
        month_text = self.date_month.currentText().strip()

        # Convert month name to month number (1-12)
        month_map = {
            "january": 1, "february": 2, "march": 3, "april": 4,
            "may": 5, "june": 6, "july": 7, "august": 8,
            "september": 9, "october": 10, "november": 11, "december": 12
        }

        try:
            day = int(day_text)
        except ValueError:
            day = -1

        try:
            year = int(year_text)
        except ValueError:
            year = -1

        month_num = month_map.get(month_text.lower(), -1)

        # Build a YYYY-MM-DD string if we can, otherwise pass something that will fail validation
        if year > 0 and month_num > 0 and day > 0:
            date_str = f"{year:04d}-{month_num:02d}-{day:02d}"
        else:
            date_str = "INVALID"

        # --- Exercise: HH + MM -> total minutes ---
        ex_h = int(self.exercise_hours.text() or 0)
        ex_m = int(self.exercise_minutes.text() or 0)
        exercise_total_minutes = ex_h * 60 + ex_m

        # --- Sleep: HH + MM -> total minutes ---
        sleep_h = int(self.sleep_hours.text() or 0)
        sleep_m = int(self.sleep_minutes.text() or 0)
        sleep_total_minutes = sleep_h * 60 + sleep_m

        # --- Other fields (placeholders for now) ---
        mood_scale_text = self.mood_scale.text().strip()

        # You haven't created these widgets yet, so keep safe placeholders for now
        mood_tags = ""      # later: self.mood_tags.text().strip()
        activities = ""     # later: self.activities.text().strip()
        notes = ""          # later: self.notes.text().strip()

        entry, errors = create_daily_entry(
            date=date_str,
            hours_slept=sleep_total_minutes,
            exercise_minutes=exercise_total_minutes,
            mood_scale=mood_scale_text,
            mood_tags=mood_tags,
            activities=activities,
            notes=notes,
        )

        if errors:
            QMessageBox.warning(
                self,
                "Fix these fields",
                "\n".join(f"{field}: {msg}" for field, msg in errors.items())
            )
            return

        QMessageBox.information(self, "Saved", f"Entry is valid:\n{entry}")




app = QApplication([])

window = InputEntryWindow()
window.show()

app.exec()


"""
For now, only start working on the "Entry input" and CSV parts of the GUI.
The graphing/visualizing stuff will be added on later, don't worry about
the code/implementation for that right now
"""