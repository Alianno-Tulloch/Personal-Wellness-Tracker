"""
entry_page_gui.py

This file contains the **Log Entry Page** of the Mental Health Tracker app.

Important design choice:
----------------------------------------------------
This is a **QWidget, NOT a QMainWindow anymore.**

Reason:
The real application will have multiple "pages"
(Log Entry, View Entries, Graphs, Import / Export, etc),
and they will all live inside one main window.

So this file ONLY cares about:
- displaying entry fields
- collecting user input
- sending raw text to data_validation.py
- saving valid entries through data_io.py
"""

import sys

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QLineEdit, QPushButton
)
from PySide6.QtGui import QIntValidator, QDoubleValidator

# Validation + parsing logic lives here
from data_validation import create_daily_entry

# File I/O and CSV logic lives here
from data_io import upsert_entry


# ================================================================
# Where the CSV lives while developing.
# This path is used by ALL entry saves.
# ================================================================
CSV_PATH = "data/entries.csv"



class EntryPage(QWidget):
    """
    This class represents the **Log Entry Page**.

    It is responsible for:
    - Taking user input
    - Showing validation errors
    - Calling create_daily_entry(...) to validate + parse
    - Calling upsert_entry(...) to save the entry

    NOTE:
    This widget does NOT know or care about:
    - Menus
    - Other pages
    - Windows
    - Graphs
    - Tables
    """

    def __init__(self, parent=None):
        # Initialize QWidget normally
        super().__init__(parent)

        # ================================================================
        # MAIN VERTICAL LAYOUT FOR THE PAGE
        # ================================================================
        # Everything on this page is stacked vertically.
        #
        # Since this class *is* the widget, we pass `self` to QVBoxLayout.
        # ================================================================
        main_layout = QVBoxLayout(self)



        # ================================================================
        # GLOBAL ERROR PANEL
        # ================================================================
        # This label prints **ALL errors together** for accessibility,
        # so the user doesn’t need to hunt around the form.
        # ================================================================
        self.error_panel = QLabel("")
        self.error_panel.setWordWrap(True)           # long text wraps nicely
        self.error_panel.setStyleSheet("color: red;")  # make it obvious
        main_layout.addWidget(self.error_panel)



        # ================================================================
        # STATUS LABEL
        # ================================================================
        # Used to display things like:
        #   "Saved entry for 2026-01-02"
        # ================================================================
        self.status_label = QLabel("")
        main_layout.addWidget(self.status_label)



        # ================================================================
        # DATE INPUT SECTION
        # ================================================================
        main_layout.addWidget(QLabel("Enter the date:"))

        date_layout = QHBoxLayout()  # Horizontal row



        # ---- Day Input ----
        self.date_day = QLineEdit()
        self.date_day.setPlaceholderText("Day")
        self.date_day.setValidator(QIntValidator(1, 31, self))   # only 1–31



        # ---- Month Dropdown (Combo Box) ----
        self.date_month = QComboBox()
        self.date_month.setEditable(True)  # allows typing + choosing
        self.date_month.addItems([
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ])



        # ---- Year Input ----
        self.date_year = QLineEdit()
        self.date_year.setPlaceholderText("Year")
        self.date_year.setValidator(QIntValidator(1900, 2100, self))



        # ---- Add all date widgets to the row ----
        date_layout.addWidget(QLabel("Day"))
        date_layout.addWidget(self.date_day)
        date_layout.addWidget(QLabel("Month"))
        date_layout.addWidget(self.date_month)
        date_layout.addWidget(QLabel("Year"))
        date_layout.addWidget(self.date_year)

        # ---- Add the row to the main page layout ----
        main_layout.addLayout(date_layout)



        # ---- Per-field error message for date ----
        self.date_error = QLabel("")
        self.date_error.setStyleSheet("color: red;")
        main_layout.addWidget(self.date_error)



        # ================================================================
        # SLEEP ENTRY SECTION
        # ================================================================
        main_layout.addWidget(QLabel("Sleep time:"))

        sleep_layout = QHBoxLayout()

        # HH textbox
        self.sleep_hours = QLineEdit()
        self.sleep_hours.setPlaceholderText("Hours")
        self.sleep_hours.setValidator(QIntValidator(0, 24, self))

        # MM textbox
        self.sleep_minutes = QLineEdit()
        self.sleep_minutes.setPlaceholderText("Minutes")
        self.sleep_minutes.setValidator(QIntValidator(0, 59, self))

        # Add widgets to row
        sleep_layout.addWidget(QLabel("Hours"))
        sleep_layout.addWidget(self.sleep_hours)
        sleep_layout.addWidget(QLabel("Minutes"))
        sleep_layout.addWidget(self.sleep_minutes)

        main_layout.addLayout(sleep_layout)

        # Error text for this section
        self.sleep_error = QLabel("")
        self.sleep_error.setStyleSheet("color: red;")
        main_layout.addWidget(self.sleep_error)



        # ================================================================
        # EXERCISE ENTRY SECTION
        # ================================================================
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



        # ================================================================
        # MOOD SCALE INPUT
        # ================================================================
        main_layout.addWidget(QLabel("Mood scale (0.0 to 10.0):"))

        self.mood_scale = QLineEdit()
        self.mood_scale.setPlaceholderText("Example: 7.5")
        self.mood_scale.setValidator(QDoubleValidator(0.0, 10.0, 1, self))

        main_layout.addWidget(self.mood_scale)

        self.mood_scale_error = QLabel("")
        self.mood_scale_error.setStyleSheet("color: red;")
        main_layout.addWidget(self.mood_scale_error)



        # ================================================================
        # MOOD TAGS INPUT (Required)
        # ================================================================
        main_layout.addWidget(QLabel("Mood tags (comma-separated, required):"))

        self.mood_tags = QLineEdit()
        self.mood_tags.setPlaceholderText("Example: stressed, productive")
        main_layout.addWidget(self.mood_tags)

        self.mood_tags_error = QLabel("")
        self.mood_tags_error.setStyleSheet("color: red;")
        main_layout.addWidget(self.mood_tags_error)



        # ================================================================
        # ACTIVITIES INPUT (Required)
        # ================================================================
        main_layout.addWidget(QLabel("Activities (comma-separated, required):"))

        self.activities = QLineEdit()
        self.activities.setPlaceholderText("Example: studying, gym, music")
        main_layout.addWidget(self.activities)

        self.activities_error = QLabel("")
        self.activities_error.setStyleSheet("color: red;")
        main_layout.addWidget(self.activities_error)



        # ================================================================
        # NOTES INPUT (Optional)
        # ================================================================
        main_layout.addWidget(QLabel("Notes (optional):"))

        self.notes = QLineEdit()
        self.notes.setPlaceholderText("Optional")
        main_layout.addWidget(self.notes)



        # ================================================================
        # SUBMIT BUTTON
        # ================================================================
        self.submit_button = QPushButton("Submit Entry")

        # When the button is clicked, run submit_entry()
        self.submit_button.clicked.connect(self.submit_entry)

        main_layout.addWidget(self.submit_button)



    # ================================================================
    # HELPER METHODS
    # ================================================================

    def clear_errors(self) -> None:
        """
        Clear ALL red error labels + global panel.
        Called BEFORE validating a new submission.
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
        Display validation errors in TWO places:

        1) error_panel (top of page)
           - all errors listed together
           - accessibility friendly

        2) field-specific errors under each section
           - easier for the user to see where to fix things
        """

        # Build the global list
        all_lines = []
        for field, msg in errors.items():
            all_lines.append(f"{field}: {msg}")

        self.error_panel.setText("\n".join(all_lines))


        # Field-specific messages
        if "date" in errors or "date_day" in errors or "date_month" in errors or "date_year" in errors:
            parts = []
            for key in ["date_day", "date_month", "date_year", "date"]:
                if key in errors:
                    parts.append(errors[key])
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
        Called when "Submit Entry" is clicked.

        VERY IMPORTANT DESIGN RULE:
        ----------------------------------------------------
        The GUI ONLY collects RAW TEXT VALUES.
        It does NOT parse or validate logic itself.

        Instead:
        - send text to create_daily_entry(...)
        - receive clean entry dict OR error dict
        """

        # Reset previous error text
        self.clear_errors()

        # Ask validation module to process raw inputs
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

        # If validation failed → display errors → stop here
        if errors:
            self.show_errors(errors)
            return


        # Otherwise, save valid entry into CSV
        action = upsert_entry(CSV_PATH, entry)

        # Show confirmation
        self.status_label.setText(f"Saved: entry {action} for {entry['date']}")

        # Reset form fields (date left as-is for convenience)
        self.sleep_hours.clear()
        self.sleep_minutes.clear()
        self.exercise_hours.clear()
        self.exercise_minutes.clear()
        self.mood_scale.clear()
        self.mood_tags.clear()
        self.activities.clear()
        self.notes.clear()



# ================================================================
# Optional: allow this page to be run directly for testing
# ================================================================
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    page = EntryPage()
    page.show()
    sys.exit(app.exec())
