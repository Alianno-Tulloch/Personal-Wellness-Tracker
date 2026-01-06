"""
view_entries_page.py

Page for:
    - viewing all saved entries
    - (later) filtering and sorting

Visual structure:
    [ Filter row (future) ]
    [ "Expand all" / "Collapse all" buttons ]
    [ Scroll area with a vertical list of entry widgets ]
"""

from typing import List, Dict

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QFrame
)
from PySide6.QtCore import Qt, Slot

from data_io import read_entries  # you already have this
from data_formatting import minutes_to_hhmm  # helper for pretty time

CSV_PATH = "data/entries.csv"

class EntryWidget(QFrame):
    """
    One entry in the "View Entries" list.

    Has:
        - header row: date + a short summary (for example, mood and sleep)
        - details area: all fields, initially hidden

    Clicking the header toggles the details area.
    """

    def __init__(self, entry: Dict[str, str], parent: QWidget | None = None):
        super().__init__(parent)

        # Make it look like a card
        self.setFrameShape(QFrame.StyledPanel)

        self.entry = entry

        layout = QVBoxLayout(self)

        # ---------------- Header row ----------------
        header_row = QHBoxLayout()

        """
        Example of what to show in the header:
            - Date
            - Mood scale
            - Short summary of sleep
        You can change this later if you prefer a different summary.
        """

        date_label = QLabel(entry.get("date", "Unknown date"))
        date_label.setStyleSheet("font-weight: bold;")

        mood_value = entry.get("mood_scale", "")
        mood_label = QLabel(f"Mood: {mood_value}" if mood_value != "" else "Mood: n/a")

        # Sleep is stored in minutes, so we convert it back to HH:MM for display
        sleep_minutes_str = entry.get("sleep_minutes", "")
        sleep_summary = "Sleep: n/a"
        if sleep_minutes_str not in ("", None):
            try:
                sleep_minutes_int = int(float(sleep_minutes_str))
                sleep_hhmm = minutes_to_hhmm(sleep_minutes_int)
                sleep_summary = f"Sleep: {sleep_hhmm}"
            except ValueError:
                pass
        sleep_label = QLabel(sleep_summary)

        # Clicking the whole header should toggle details
        self.header_button = QPushButton()
        self.header_button.setFlat(True)  # flat so it looks like plain text
        self.header_button.setLayout(header_row)

        header_row.addWidget(date_label)
        header_row.addStretch()
        header_row.addWidget(mood_label)
        header_row.addSpacing(20)
        header_row.addWidget(sleep_label)

        layout.addWidget(self.header_button)

        # ---------------- Details area ----------------
        self.details_widget = QWidget()
        details_layout = QVBoxLayout(self.details_widget)

        """
        Add one label per field, in a simple "Field: value" format.
        You can style or reformat these later.
        """

        def add_field_label(label_text: str, key: str):
            value = self.entry.get(key, "")
            details_label = QLabel(f"{label_text}: {value if value != '' else 'n/a'}")
            details_layout.addWidget(details_label)

        add_field_label("Date", "date")
        add_field_label("Sleep (minutes)", "sleep_minutes")
        add_field_label("Exercise (minutes)", "exercise_minutes")
        add_field_label("Mood scale", "mood_scale")
        add_field_label("Mood tags", "mood_tags")
        add_field_label("Activities", "activities")
        add_field_label("Notes", "notes")

        layout.addWidget(self.details_widget)

        # Start collapsed (details hidden)
        self.details_widget.setVisible(False)

        # Connect header click -> toggle details
        self.header_button.clicked.connect(self.toggle_details)

    @Slot()
    def toggle_details(self) -> None:
        """
        Show details if hidden, hide if shown.
        """
        currently_visible = self.details_widget.isVisible()
        self.details_widget.setVisible(not currently_visible)


class ViewEntriesPage(QWidget):
    """
    The full "View Entries" page widget.

    Responsibilities:
        - Load entries from CSV (through data_io.read_entries)
        - Create an EntryWidget for each
        - Support "Expand all" / "Collapse all"
        - (Later) support filters and sorting
    """

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        main_layout = QVBoxLayout(self)

        # ---------------- Controls row ----------------
        controls_row = QHBoxLayout()

        """
        Future space for filters:
            - date range
            - min mood
            - show only entries with certain tags
        For now, we just add Expand/Collapse buttons.
        """

        self.expand_all_button = QPushButton("Expand all")
        self.collapse_all_button = QPushButton("Collapse all")

        self.expand_all_button.clicked.connect(self.expand_all)
        self.collapse_all_button.clicked.connect(self.collapse_all)

        controls_row.addWidget(self.expand_all_button)
        controls_row.addWidget(self.collapse_all_button)
        controls_row.addStretch()

        main_layout.addLayout(controls_row)

        # ---------------- Scroll area with entries ----------------
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # Container inside the scroll area that holds all EntryWidgets
        self.entries_container = QWidget()
        self.entries_layout = QVBoxLayout(self.entries_container)
        self.entries_layout.addStretch()  # keeps items at top

        self.scroll_area.setWidget(self.entries_container)
        main_layout.addWidget(self.scroll_area)

        # Keep track of EntryWidget objects so we can expand/collapse them
        self.entry_widgets: List[EntryWidget] = []

        # Initial load
        self.load_entries()

    def load_entries(self) -> None:
        """
        Load all entries from CSV (or SQLite later) and rebuild the list.
        """

        # Remove old widgets from layout
        for w in self.entry_widgets:
            w.setParent(None)
        self.entry_widgets.clear()

        # Read entries from CSV
        entries = read_entries(CSV_PATH)

        # Sort by date ascending (change later if you want newest first)
        entries.sort(key=lambda e: e.get("date", ""))

        # Rebuild entry widgets
        for entry in entries:
            widget = EntryWidget(entry, parent=self.entries_container)
            self.entries_layout.insertWidget(self.entries_layout.count() - 1, widget)
            self.entry_widgets.append(widget)


    def expand_all(self) -> None:
        """
        Show details for every entry.
        """
        for w in self.entry_widgets:
            w.details_widget.setVisible(True)

    def collapse_all(self) -> None:
        """
        Hide details for every entry.
        """
        for w in self.entry_widgets:
            w.details_widget.setVisible(False)
