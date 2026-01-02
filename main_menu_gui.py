"""
main_window_gui.py

This file contains the **Main Application Window**
for the Mental Health Tracker.

This is the "shell" or "frame" of the app.

Responsibilities:
----------------------------------------------------
- Displays a row of navigation buttons (like tabs)
- Holds a QStackedWidget to switch between pages
- Creates and owns each page:
    • EntryPage
    • EntriesListPage (placeholder for now)
    • GraphsPage (placeholder for now)
    • ImportExportPage (placeholder for now)

This file SHOULD NOT care about:
- how entries are saved
- how validation works
- the details inside each page

Each page manages itself.
"""


import sys

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget
)
from PySide6.QtCore import Qt

# Import the Log Entry page
from entry_page_gui import EntryPage



class MainWindow(QMainWindow):
    """
    The MainWindow is the "root" of the entire GUI application.
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mental Health Tracker - Main Menu")
        self.resize(900, 700)



        # ================================================================
        # CENTRAL WIDGET + MASTER LAYOUT
        # ================================================================
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)

        # Attach layout to the central widget
        self.setCentralWidget(central_widget)



        # ================================================================
        # TOP NAVIGATION BUTTONS (like a menu bar)
        # ================================================================
        nav_layout = QHBoxLayout()

        # Buttons for each page
        self.entry_button = QPushButton("Log Entry")
        self.view_entries_button = QPushButton("View Entries")
        self.graphs_button = QPushButton("Graphs")
        self.import_export_button = QPushButton("Import / Export")

        # Add buttons to the row
        nav_layout.addWidget(self.entry_button)
        nav_layout.addWidget(self.view_entries_button)
        nav_layout.addWidget(self.graphs_button)
        nav_layout.addWidget(self.import_export_button)

        # Add the nav bar to the main layout
        main_layout.addLayout(nav_layout)



        # ================================================================
        # STACKED WIDGET = PAGE CONTAINER
        # ================================================================
        # This is the core of navigation:
        #
        # QStackedWidget holds multiple pages
        # but only shows ONE page at a time.
        # ================================================================
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)



        # ================================================================
        # CREATE AND ADD PAGES
        # ================================================================

        # Real page
        self.entry_page = EntryPage()

        # Temporary placeholder pages
        self.entries_list_page = self._make_placeholder_page("Entries list page (COMING SOON)")
        self.graphs_page = self._make_placeholder_page("Graphs page (COMING SOON)")
        self.import_export_page = self._make_placeholder_page("Import / Export page (COMING SOON)")


        # Order matters: these are the pages in the stack
        self.stack.addWidget(self.entry_page)          # index 0
        self.stack.addWidget(self.entries_list_page)   # index 1
        self.stack.addWidget(self.graphs_page)         # index 2
        self.stack.addWidget(self.import_export_page)  # index 3



        # ================================================================
        # CONNECT BUTTONS TO PAGE SWITCHING
        # ================================================================
        self.entry_button.clicked.connect(self.show_entry_page)
        self.view_entries_button.clicked.connect(self.show_entries_list_page)
        self.graphs_button.clicked.connect(self.show_graphs_page)
        self.import_export_button.clicked.connect(self.show_import_export_page)



        # ================================================================
        # DEFAULT PAGE
        # ================================================================
        self.show_entry_page()



    # ================================================================
    # UTILITY: BUILD A PLACEHOLDER PAGE
    # ================================================================
    def _make_placeholder_page(self, text: str) -> QWidget:
        """
        Creates a temporary simple page containing centered text.

        This lets us see page switching working,
        even before we've built the real UI for that page.
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
# APPLICATION ENTRY POINT
# ================================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
