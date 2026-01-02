"""
main_menu_gui.py

Main application window for the Personal Wellness Tracker.

Layout:
----------------------------------------------------
[ Sidebar (left) ]  [  Main content area (pages)   ]

Sidebar:
    - "Menu" button (collapse / expand)
    - Navigation buttons:
        • Log Entry
        • View Entries
        • Graphs
        • Import / Export

Main content:
    - QStackedWidget that shows one page at a time:
        • EntryPage (real)
        • EntriesListPage (placeholder)
        • GraphsPage (placeholder)
        • ImportExportPage (placeholder)
"""

import sys

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget
)
from PySide6.QtCore import Qt

# Import the Log Entry page (the QWidget we built earlier)
from entry_page_gui import EntryPage


class MainWindow(QMainWindow):
    """
    The MainWindow is the "shell" around all pages.

    It knows:
        - how to lay out the sidebar and content
        - how to switch which page is visible

    It does NOT know:
        - how validation works
        - how saving works
        - what each page does internally
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Personal Wellness Tracker")
        self.resize(1000, 700)

        # ================================================================
        # CENTRAL WIDGET + ROOT LAYOUT
        # ================================================================
        # QMainWindow needs a single central widget.
        # That central widget gets a horizontal layout:
        #
        #   [ sidebar_widget ]  [ stacked_pages ]
        # ================================================================
        central_widget = QWidget()
        root_layout = QHBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        # We will keep a reference to the sidebar so we can hide/show it.
        self.sidebar_widget = QWidget()
        sidebar_layout = QVBoxLayout(self.sidebar_widget)

        # Optional: give the sidebar a fixed-ish width so it feels like a panel
        self.sidebar_widget.setFixedWidth(200)

        # Add the sidebar to the left side of the root layout
        root_layout.addWidget(self.sidebar_widget)

        # ================================================================
        # SIDEBAR: MENU TOGGLE BUTTON
        # ================================================================
        # "Menu" button at the top that can hide/show the sidebar.
        # When hidden, only the content area remains.
        # ================================================================
        self.menu_toggle_button = QPushButton("Hide Menu")
        self.menu_toggle_button.clicked.connect(self.toggle_sidebar)
        sidebar_layout.addWidget(self.menu_toggle_button)

        # Small spacer label for separation
        sidebar_layout.addWidget(QLabel("Navigation:"))

        # ================================================================
        # SIDEBAR: NAVIGATION BUTTONS
        # ================================================================
        self.entry_button = QPushButton("Log Entry")
        self.view_entries_button = QPushButton("View Entries")
        self.graphs_button = QPushButton("Graphs")
        self.import_export_button = QPushButton("Import / Export")

        # Add nav buttons to the sidebar (vertical)
        sidebar_layout.addWidget(self.entry_button)
        sidebar_layout.addWidget(self.view_entries_button)
        sidebar_layout.addWidget(self.graphs_button)
        sidebar_layout.addWidget(self.import_export_button)

        # Add a stretch at the bottom so buttons stay at the top
        sidebar_layout.addStretch()

        # ================================================================
        # MAIN CONTENT: STACKED WIDGET (PAGES)
        # ================================================================
        # This is the area on the right that changes when nav buttons are clicked.
        # ================================================================
        self.stack = QStackedWidget()
        root_layout.addWidget(self.stack, stretch=1)  # stretch=1 so it takes remaining space

        # ================================================================
        # CREATE PAGES
        # ================================================================
        self.entry_page = EntryPage()

        # Placeholder pages for now (simple labels)
        self.entries_list_page = self._make_placeholder_page("Entries list page (COMING SOON)")
        self.graphs_page = self._make_placeholder_page("Graphs page (COMING SOON)")
        self.import_export_page = self._make_placeholder_page("Import / Export page (COMING SOON)")

        # Add pages to the stack
        self.stack.addWidget(self.entry_page)          # index 0
        self.stack.addWidget(self.entries_list_page)   # index 1
        self.stack.addWidget(self.graphs_page)         # index 2
        self.stack.addWidget(self.import_export_page)  # index 3

        # ================================================================
        # CONNECT NAV BUTTONS TO PAGE SWITCHING
        # ================================================================
        self.entry_button.clicked.connect(self.show_entry_page)
        self.view_entries_button.clicked.connect(self.show_entries_list_page)
        self.graphs_button.clicked.connect(self.show_graphs_page)
        self.import_export_button.clicked.connect(self.show_import_export_page)

        # Start on the Log Entry page
        self.show_entry_page()

    # ================================================================
    # HELPER: PLACEHOLDER PAGE
    # ================================================================
    def _make_placeholder_page(self, text: str) -> QWidget:
        """
        Simple helper that creates a QWidget with a centered label.

        Used until proper pages (tables, graphs, etc) are implemented.
        """
        page = QWidget()
        layout = QVBoxLayout(page)

        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)

        layout.addWidget(label)
        return page

    # ================================================================
    # PAGE SWITCHING METHODS
    # ================================================================
    def show_entry_page(self) -> None:
        self.stack.setCurrentWidget(self.entry_page)

    def show_entries_list_page(self) -> None:
        self.stack.setCurrentWidget(self.entries_list_page)

    def show_graphs_page(self) -> None:
        self.stack.setCurrentWidget(self.graphs_page)

    def show_import_export_page(self) -> None:
        self.stack.setCurrentWidget(self.import_export_page)

    # ================================================================
    # SIDEBAR TOGGLE
    # ================================================================
    def toggle_sidebar(self) -> None:
        """
        Show / hide the sidebar widget.

        When hidden:
            - only the main content area is visible
            - button text changes to "Show Menu"
        """
        is_visible = self.sidebar_widget.isVisible()

        if is_visible:
            # Hide the sidebar
            self.sidebar_widget.hide()
            self.menu_toggle_button.setText("Show Menu")
        else:
            # Show the sidebar
            self.sidebar_widget.show()
            self.menu_toggle_button.setText("Hide Menu")


# ================================================================
# APPLICATION ENTRY POINT
# ================================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
