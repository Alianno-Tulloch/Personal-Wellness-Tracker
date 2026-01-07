"""
view_entries_page.py

Page for:
    - viewing all saved entries
    - sorting by basic fields (date / mood / sleep / exercise)
    - choosing what shows in the collapsed header (mood / sleep / exercise)

Visual structure:
    [ Controls row: expand/collapse + sort controls ]
    [ Header-toggle row: which fields to show in summary ]
    [ Scroll area with a vertical list of entry widgets ]
"""

from typing import List, Dict

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QFrame, QComboBox, QCheckBox
)
from PySide6.QtCore import Qt, Slot

from data_io import read_entries
from data_formatting import minutes_to_human, iso_date_to_human

# Same CSV path convention as the rest of the project
CSV_PATH = "data/entries.csv"


class EntryWidget(QFrame):
    """
    One entry in the "View Entries" list.

    Has:
        - header row: date + short summary (mood + sleep + exercise)
        - details area: all fields, initially hidden

    Clicking the header toggles the details area.
    """

    def __init__(self, entry: Dict[str, str], parent: QWidget | None = None):
        super().__init__(parent)

        # Make this look like a "card" instead of a plain label
        self.setFrameShape(QFrame.StyledPanel)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 14, 10, 14)
        layout.setSpacing(10)

        # ------------------------------------------------
        # Header row - always visible
        # ------------------------------------------------
        header_row = QHBoxLayout()

        # --- Date (human friendly) ---
        raw_date = entry.get("date", "")
        if raw_date:
            # Uses your iso_date_to_human, e.g. "01 January 2025"
            human_date = iso_date_to_human(raw_date)
        else:
            human_date = "Unknown date"

        self.date_label = QLabel(human_date)
        self.date_label.setStyleSheet("font-weight: bold;")

        # --- Mood summary ---
        mood_value = entry.get("mood_scale", "")
        if mood_value != "":
            mood_text = f"Mood: {mood_value}"
        else:
            mood_text = "Mood: n/a"
        self.mood_label = QLabel(mood_text)

        # --- Sleep summary (stored as minutes) ---
        sleep_minutes_str = entry.get("sleep_minutes", "")
        sleep_summary = "Sleep: n/a"
        if sleep_minutes_str not in ("", None):
            try:
                sleep_minutes_int = int(float(sleep_minutes_str))
                if sleep_minutes_int >= 0:
                    # Compact human format, e.g. "7h 30mins"
                    sleep_human = minutes_to_human(sleep_minutes_int, 1)
                    if not sleep_human:
                        # If helper returns empty for 0 minutes, fall back
                        sleep_human = "0 mins"
                    sleep_summary = f"Sleep: {sleep_human}"
            except ValueError:
                # If something weird is in the CSV, just leave as "n/a"
                pass
        self.sleep_label = QLabel(sleep_summary)

        # --- Exercise summary (stored as minutes) ---
        exercise_minutes_str = entry.get("exercise_minutes", "")
        exercise_summary = "Exercise: n/a"
        if exercise_minutes_str not in ("", None):
            try:
                exercise_minutes_int = int(float(exercise_minutes_str))
                if exercise_minutes_int >= 0:
                    exercise_human = minutes_to_human(exercise_minutes_int, 1)
                    if not exercise_human:
                        exercise_human = "0 mins"
                    exercise_summary = f"Exercise: {exercise_human}"
            except ValueError:
                pass
        self.exercise_label = QLabel(exercise_summary)

        # Make the whole header clickable (not just tiny text)
        self.header_button = QPushButton()
        self.header_button.setFlat(True)
        self.header_button.setLayout(header_row)

        # Make the row itself taller so the bigger font fits comfortably
        self.header_button.setMinimumHeight(40)  # try 40–48 and see what looks best

        self.header_button.setFlat(True)  # looks like plain text
        self.header_button.setLayout(header_row)

        # Header layout: [Date]  [stretch]  [Mood]  [Sleep]  [Exercise]
        header_row.addWidget(self.date_label)
        header_row.addStretch()
        header_row.addWidget(self.mood_label)
        header_row.addSpacing(16)
        header_row.addWidget(self.sleep_label)
        header_row.addSpacing(16)
        header_row.addWidget(self.exercise_label)

        layout.addWidget(self.header_button)

        # ------------------------------------------------
        # Details area - hidden by default
        # ------------------------------------------------
        self.details_widget = QWidget()
        details_layout = QVBoxLayout(self.details_widget)

        def add_field_label(label_text: str, key: str) -> None:
            """
            Small helper so all detail rows look consistent.
            Shows a label on the left and the raw value on the right.
            """
            row = QHBoxLayout()
            lbl = QLabel(label_text)
            val = QLabel(str(entry.get(key, "")))
            row.addWidget(lbl)
            row.addStretch()
            row.addWidget(val)
            details_layout.addLayout(row)

        # Show every column from the CSV in the details
        add_field_label("Date", "date")
        add_field_label("Sleep (minutes)", "sleep_minutes")
        add_field_label("Exercise (minutes)", "exercise_minutes")
        add_field_label("Mood scale", "mood_scale")
        add_field_label("Mood tags", "mood_tags")
        add_field_label("Activities", "activities")
        add_field_label("Notes", "notes")

        layout.addWidget(self.details_widget)

        # Start with details hidden (collapsed)
        self.details_widget.setVisible(False)

        # Connect header click -> toggle details
        self.header_button.clicked.connect(self.toggle_details)

    def set_header_visibility(
        self,
        show_mood: bool,
        show_sleep: bool,
        show_exercise: bool,
    ) -> None:
        """
        Called by the parent page when the user toggles which fields to
        show in the collapsed summary row.
        """
        self.mood_label.setVisible(show_mood)
        self.sleep_label.setVisible(show_sleep)
        self.exercise_label.setVisible(show_exercise)

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
        - Load entries from CSV via data_io.read_entries
        - Create an EntryWidget for each
        - Support "Expand all" / "Collapse all"
        - Support sorting by date / mood / sleep / exercise
        - Let the user choose what shows in the summary row
    """

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        main_layout = QVBoxLayout(self)

        # ------------------------------------------------
        # Controls row: expand/collapse + sort controls
        # ------------------------------------------------
        controls_row = QHBoxLayout()

        # Expand / collapse buttons
        expand_btn = QPushButton("Expand all")
        collapse_btn = QPushButton("Collapse all")
        expand_btn.clicked.connect(self.expand_all)
        collapse_btn.clicked.connect(self.collapse_all)

        controls_row.addWidget(expand_btn)
        controls_row.addWidget(collapse_btn)

        # Sort controls
        sort_label = QLabel("Sort by:")

        # This combo box chooses WHICH field to sort on
        self.sort_field_combo = QComboBox()
        # The user-visible text is the label, userData is the key name.
        self.sort_field_combo.addItem("Date", "date")
        self.sort_field_combo.addItem("Mood", "mood")
        self.sort_field_combo.addItem("Sleep", "sleep")
        self.sort_field_combo.addItem("Exercise", "exercise")

        # This combo chooses ascending vs descending
        self.sort_order_combo = QComboBox()
        self.sort_order_combo.addItem("Ascending", "asc")
        self.sort_order_combo.addItem("Descending", "desc")

        # Whenever sort settings change, we reload entries.
        self.sort_field_combo.currentIndexChanged.connect(self.load_entries)
        self.sort_order_combo.currentIndexChanged.connect(self.load_entries)

        controls_row.addSpacing(20)
        controls_row.addWidget(sort_label)
        controls_row.addWidget(self.sort_field_combo)
        controls_row.addWidget(self.sort_order_combo)
        controls_row.addStretch()

        main_layout.addLayout(controls_row)

        # ------------------------------------------------
        # Header-summary toggle row: which fields show in collapsed text
        # ------------------------------------------------
        header_toggle_row = QHBoxLayout()
        header_toggle_row.addWidget(QLabel("Show in summary:"))

        self.show_mood_checkbox = QCheckBox("Mood")
        self.show_mood_checkbox.setChecked(True)

        self.show_sleep_checkbox = QCheckBox("Sleep")
        self.show_sleep_checkbox.setChecked(True)

        self.show_exercise_checkbox = QCheckBox("Exercise")
        self.show_exercise_checkbox.setChecked(True)

        # Any time these change, we update all header rows.
        self.show_mood_checkbox.stateChanged.connect(self.apply_header_visibility)
        self.show_sleep_checkbox.stateChanged.connect(self.apply_header_visibility)
        self.show_exercise_checkbox.stateChanged.connect(self.apply_header_visibility)

        header_toggle_row.addWidget(self.show_mood_checkbox)
        header_toggle_row.addWidget(self.show_sleep_checkbox)
        header_toggle_row.addWidget(self.show_exercise_checkbox)
        header_toggle_row.addStretch()

        main_layout.addLayout(header_toggle_row)

        # ------------------------------------------------
        # Scroll area with all entry widgets
        # ------------------------------------------------
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # Container inside the scroll area that holds all EntryWidgets
        self.entries_container = QWidget()
        self.entries_layout = QVBoxLayout(self.entries_container)
        # Stretch at the bottom keeps items pinned to the top
        self.entries_layout.addStretch()

        self.scroll_area.setWidget(self.entries_container)
        main_layout.addWidget(self.scroll_area)

        # Keep track of EntryWidgets so we can expand/collapse and
        # apply header-visibility toggles later.
        self.entry_widgets: List[EntryWidget] = []

        # Initial load
        self.load_entries()

    # ------------------------------------------------
    # Sorting helpers
    # ------------------------------------------------

    def _current_sort_field(self) -> str:
        """
        Return the internal field name chosen in the sort combo.
        """
        data = self.sort_field_combo.currentData()
        # Default to date if weirdly None
        return data if data is not None else "date"

    def _current_sort_reverse(self) -> bool:
        """
        True if we should sort in descending order.
        """
        return self.sort_order_combo.currentData() == "desc"

    @staticmethod
    def _safe_int(value: str) -> int:
        """
        Convert a string to int safely. If it fails, default to -1.

        Using -1 means "unknown" values end up at the start of ascending lists
        and at the end of descending lists, which is fine for this use case.
        """
        try:
            return int(float(value))
        except Exception:
            return -1

    @staticmethod
    def _safe_float(value: str) -> float:
        """
        Convert a string to float safely. If it fails, default to -1.0.
        """
        try:
            return float(value)
        except Exception:
            return -1.0

    def _sort_key(self, entry: Dict[str, str]):
        """
        Compute the key to use when sorting a single entry, based on
        the current sort settings (field + order).
        """
        field = self._current_sort_field()

        if field == "mood":
            return self._safe_float(entry.get("mood_scale", ""))
        if field == "sleep":
            return self._safe_int(entry.get("sleep_minutes", ""))
        if field == "exercise":
            return self._safe_int(entry.get("exercise_minutes", ""))

        # Default: sort by date (YYYY-MM-DD strings sort chronologically)
        return entry.get("date", "")

    # ------------------------------------------------
    # Core loading / refreshing
    # ------------------------------------------------

    def load_entries(self) -> None:
        """
        Load all entries from CSV (or SQLite in the future), apply
        the current sort choice, and rebuild the list of EntryWidgets.
        """
        # Remove old widgets from layout
        for w in self.entry_widgets:
            w.setParent(None)
        self.entry_widgets.clear()

        # Pull entries from CSV
        entries = read_entries(CSV_PATH)

        # Sort entries based on user's choices
        entries.sort(key=self._sort_key, reverse=self._current_sort_reverse())

        # Summary visibility choices (we reuse these for every widget)
        show_mood = self.show_mood_checkbox.isChecked()
        show_sleep = self.show_sleep_checkbox.isChecked()
        show_exercise = self.show_exercise_checkbox.isChecked()

        # Rebuild entry widgets
        for entry in entries:
            widget = EntryWidget(entry, parent=self.entries_container)
            # Insert above the final stretch item
            self.entries_layout.insertWidget(self.entries_layout.count() - 1, widget)
            widget.set_header_visibility(show_mood, show_sleep, show_exercise)
            self.entry_widgets.append(widget)

    # ------------------------------------------------
    # Header visibility helpers
    # ------------------------------------------------

    def apply_header_visibility(self) -> None:
        """
        Called when the user toggles any of the "Show in summary" checkboxes.
        Applies the visibility choice to all existing EntryWidgets.
        """
        show_mood = self.show_mood_checkbox.isChecked()
        show_sleep = self.show_sleep_checkbox.isChecked()
        show_exercise = self.show_exercise_checkbox.isChecked()

        for w in self.entry_widgets:
            w.set_header_visibility(show_mood, show_sleep, show_exercise)

    # ------------------------------------------------
    # Expand / collapse helpers
    # ------------------------------------------------

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
