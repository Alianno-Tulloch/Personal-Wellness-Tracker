import sys

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QLineEdit, QPushButton, QMainWindow
)
from PySide6.QtGui import QIntValidator, QDoubleValidator

from data_validation import create_daily_entry
from data_io import upsert_entry


# Where your CSV lives during development.
# Packaging later can change this, but this is fine for now.
CSV_PATH = "data/entries.csv"


class InputEntryWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mental Health Tracker App")
        self.resize(700, 650)

        # Central widget is required for QMainWindow layouts.
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        # ---------------------------------------
        # Global error panel (shows ALL errors)
        # ---------------------------------------
        self.error_panel = QLabel("")
        self.error_panel.setWordWrap(True)

        # Red text to make errors obvious.
        self.error_panel.setStyleSheet("color: red;")
        main_layout.addWidget(self.error_panel)

        # Small status label (for "Saved" / "Updated" messages)
        self.status_label = QLabel("")
        main_layout.addWidget(self.status_label)

        # ---------------------------------------
        # Date section (3 inputs)
        # ---------------------------------------
        main_layout.addWidget(QLabel("Enter the date:"))

        date_layout = QHBoxLayout()

        self.date_day = QLineEdit()
        self.date_day.setPlaceholderText("Day")
        self.date_day.setValidator(QIntValidator(1, 31, self))

        self.date_month = QComboBox()
        self.date_month.setEditable(True)
        self.date_month.addItems([
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ])

        self.date_year = QLineEdit()
        self.date_year.setPlaceholderText("Year")
        self.date_year.setValidator(QIntValidator(1900, 2100, self))

        date_layout.addWidget(QLabel("Day"))
        date_layout.addWidget(self.date_day)
        date_layout.addWidget(QLabel("Month"))
        date_layout.addWidget(self.date_month)
        date_layout.addWidget(QLabel("Year"))
        date_layout.addWidget(self.date_year)

        main_layout.addLayout(date_layout)

        # Error label specifically for date issues
        self.date_error = QLabel("")
        self.date_error.setStyleSheet("color: red;")
        main_layout.addWidget(self.date_error)

        # ---------------------------------------
        # Sleep section (HH + MM, one blank allowed)
        # ---------------------------------------
        main_layout.addWidget(QLabel("Sleep time:"))

        sleep_layout = QHBoxLayout()

        self.sleep_hours = QLineEdit()
        self.sleep_hours.setPlaceholderText("Hours")
        self.sleep_hours.setValidator(QIntValidator(0, 24, self))

        self.sleep_minutes = QLineEdit()
        self.sleep_minutes.setPlaceholderText("Minutes")
        self.sleep_minutes.setValidator(QIntValidator(0, 59, self))

        sleep_layout.addWidget(QLabel("Hours"))
        sleep_layout.addWidget(self.sleep_hours)
        sleep_layout.addWidget(QLabel("Minutes"))
        sleep_layout.addWidget(self.sleep_minutes)

        main_layout.addLayout(sleep_layout)

        self.sleep_error = QLabel("")
        self.sleep_error.setStyleSheet("color: red;")
        main_layout.addWidget(self.sleep_error)

        # ---------------------------------------
        # Exercise section (HH + MM, one blank allowed)
        # ---------------------------------------
        main_layout.addWidget(QLabel("Exercise time:"))

        exercise_layout = QHBoxLayout()

        self.exercise_hours = QLineEdit()
        self.exercise_hours.setPlaceholderText("Hours")
        self.exercise_hours.setValidator(QIntValidator(0, 24, self))

        self.exercise_minutes = QLineEdit()
        self.exercise_minutes.setPlaceholderText("Minutes")
        self.exercise_minutes.setValidator(QIntValidator(0, 59, self))

        exercise_layout.addWidget(QLabel("Hours"))
        exercise_layout.addWidget(self.exercise_hours)
        exercise_layout.addWidget(QLabel("Minutes"))
        exercise_layout.addWidget(self.exercise_minutes)

        main_layout.addLayout(exercise_layout)

        self.exercise_error = QLabel("")
        self.exercise_error.setStyleSheet("color: red;")
        main_layout.addWidget(self.exercise_error)

        # ---------------------------------------
        # Mood scale section (single input, float 0.0 - 10.0)
        # ---------------------------------------
        main_layout.addWidget(QLabel("Mood scale (0.0 to 10.0):"))

        self.mood_scale = QLineEdit()
        self.mood_scale.setPlaceholderText("Example: 7.5")
        self.mood_scale.setValidator(QDoubleValidator(0.0, 10.0, 1, self))
        main_layout.addWidget(self.mood_scale)

        self.mood_scale_error = QLabel("")
        self.mood_scale_error.setStyleSheet("color: red;")
        main_layout.addWidget(self.mood_scale_error)

        # ---------------------------------------
        # Mood tags (required)
        # ---------------------------------------
        main_layout.addWidget(QLabel("Mood tags (comma-separated, required):"))

        self.mood_tags = QLineEdit()
        self.mood_tags.setPlaceholderText("Example: stressed, productive")
        main_layout.addWidget(self.mood_tags)

        self.mood_tags_error = QLabel("")
        self.mood_tags_error.setStyleSheet("color: red;")
        main_layout.addWidget(self.mood_tags_error)

        # ---------------------------------------
        # Activities (required)
        # ---------------------------------------
        main_layout.addWidget(QLabel("Activities (comma-separated, required):"))

        self.activities = QLineEdit()
        self.activities.setPlaceholderText("Example: studying, gym, music")
        main_layout.addWidget(self.activities)

        self.activities_error = QLabel("")
        self.activities_error.setStyleSheet("color: red;")
        main_layout.addWidget(self.activities_error)

        # ---------------------------------------
        # Notes (optional)
        # ---------------------------------------
        main_layout.addWidget(QLabel("Notes (optional):"))

        self.notes = QLineEdit()
        self.notes.setPlaceholderText("Optional")
        main_layout.addWidget(self.notes)

        # No error label needed for notes (optional)

        # ---------------------------------------
        # Submit button
        # ---------------------------------------
        self.submit_button = QPushButton("Submit Entry")
        self.submit_button.clicked.connect(self.submit_entry)
        main_layout.addWidget(self.submit_button)

    def clear_errors(self) -> None:
        """
        Reset all error labels.
        """
        self.error_panel.setText("")
        self.status_label.setText("")

        self.date_error.setText("")
        self.sleep_error.setText("")
        self.exercise_error.setText("")
        self.mood_scale_error.setText("")
        self.mood_tags_error.setText("")
        self.activities_error.setText("")

    def show_errors(self, errors: dict[str, str]) -> None:
        """
        Display errors:
        - global error panel: all errors at once
        - section labels: show relevant message near the field
        """
        # Global panel
        all_lines = []
        for field, msg in errors.items():
            all_lines.append(f"{field}: {msg}")
        self.error_panel.setText("\n".join(all_lines))

        # Section mapping (field keys come from data_validation.py)
        if "date" in errors or "date_day" in errors or "date_month" in errors or "date_year" in errors:
            parts = []
            for k in ["date_day", "date_month", "date_year", "date"]:
                if k in errors:
                    parts.append(errors[k])
            self.date_error.setText(" ".join(parts))

        if "sleep_time" in errors:
            self.sleep_error.setText(errors["sleep_time"])

        if "exercise_time" in errors:
            self.exercise_error.setText(errors["exercise_time"])

        if "mood_scale" in errors:
            self.mood_scale_error.setText(errors["mood_scale"])

        if "mood_tags" in errors:
            self.mood_tags_error.setText(errors["mood_tags"])

        if "activities" in errors:
            self.activities_error.setText(errors["activities"])

    def submit_entry(self) -> None:
        """
        Called when the submit button is clicked.

        Important design choice:
        - GUI collects raw strings only.
        - Parsing/validation happens in create_daily_entry.
        - If valid, we upsert to CSV.
        """
        self.clear_errors()

        entry, errors = create_daily_entry(
            date_day_text=self.date_day.text(),
            date_month_text=self.date_month.currentText(),
            date_year_text=self.date_year.text(),
            sleep_hours_text=self.sleep_hours.text(),
            sleep_minutes_text=self.sleep_minutes.text(),
            exercise_hours_text=self.exercise_hours.text(),
            exercise_minutes_text=self.exercise_minutes.text(),
            mood_scale_text=self.mood_scale.text(),
            mood_tags_text=self.mood_tags.text(),
            activities_text=self.activities.text(),
            notes_text=self.notes.text(),
        )

        if errors:
            self.show_errors(errors)
            return

        # Save to CSV (update or insert)
        action = upsert_entry(CSV_PATH, entry)
        self.status_label.setText(f"Saved: entry {action} for {entry['date']}")

        # Clear fields after save.
        # Keep date fields if you want rapid edits for the same day.
        self.sleep_hours.clear()
        self.sleep_minutes.clear()
        self.exercise_hours.clear()
        self.exercise_minutes.clear()
        self.mood_scale.clear()
        self.mood_tags.clear()
        self.activities.clear()
        self.notes.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InputEntryWindow()
    window.show()
    sys.exit(app.exec())
