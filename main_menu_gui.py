"""
main_window.py

Main window with:
    - Top bar (always visible) with a "Show/Hide Menu" button
    - Left sidebar with navigation buttons
    - Right-hand stacked pages area
"""

import sys

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget
)
from PySide6.QtCore import Qt

from entry_page import EntryPage
from view_entries_page import ViewEntriesPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Personal Wellness Tracker")
        self.resize(1000, 700)

        # ============================================================
        # CENTRAL WIDGET + OUTER (VERTICAL) LAYOUT
        # ============================================================
        # Layout structure:
        #
        # [ top_bar (menu toggle) ]
        # [ main_row:  sidebar  |  stacked pages ]
        # ============================================================
        central = QWidget()
        outer_layout = QVBoxLayout(central)
        self.setCentralWidget(central)

        # ---------------- Top bar (always visible) -------------------
        top_bar = QHBoxLayout()

        # This button is OUTSIDE the sidebar now, so it never disappears.
        self.menu_toggle_button = QPushButton("Hide Menu")
        self.menu_toggle_button.clicked.connect(self.toggle_sidebar)

        # You can add a title label here later if you want.
        title_label = QLabel("Personal Wellness Tracker")
        title_label.setAlignment(Qt.AlignCenter)

        top_bar.addWidget(self.menu_toggle_button)
        top_bar.addStretch()
        top_bar.addWidget(title_label)
        top_bar.addStretch()

        outer_layout.addLayout(top_bar)

        # ---------------- Main row: sidebar + content ----------------
        main_row = QHBoxLayout()
        outer_layout.addLayout(main_row, stretch=1)

        # ========== Sidebar ==========
        self.sidebar_widget = QWidget()
        sidebar_layout = QVBoxLayout(self.sidebar_widget)
        self.sidebar_widget.setFixedWidth(200)

        sidebar_layout.addWidget(QLabel("Navigation:"))

        self.entry_button = QPushButton("Log Entry")
        self.view_entries_button = QPushButton("View Entries")
        self.graphs_button = QPushButton("Graphs")
        self.import_export_button = QPushButton("Import / Export")

        sidebar_layout.addWidget(self.entry_button)
        sidebar_layout.addWidget(self.view_entries_button)
        sidebar_layout.addWidget(self.graphs_button)
        sidebar_layout.addWidget(self.import_export_button)
        sidebar_layout.addStretch()

        main_row.addWidget(self.sidebar_widget)

        # ========== Stacked pages ==========
        self.stack = QStackedWidget()
        main_row.addWidget(self.stack, stretch=1)

        # ============================================================
        # PAGES
        # ============================================================
        self.entry_page = EntryPage()
        self.entries_list_page = ViewEntriesPage()
        self.graphs_page = self._make_placeholder_page("Graphs page (COMING SOON)")
        self.import_export_page = self._make_placeholder_page("Import / Export page (COMING SOON)")

        self.stack.addWidget(self.entry_page)          # index 0
        self.stack.addWidget(self.entries_list_page)   # index 1
        self.stack.addWidget(self.graphs_page)         # index 2
        self.stack.addWidget(self.import_export_page)  # index 3

        # Hook nav buttons to pages
        self.entry_button.clicked.connect(self.show_entry_page)
        self.view_entries_button.clicked.connect(self.show_entries_list_page)
        self.graphs_button.clicked.connect(self.show_graphs_page)
        self.import_export_button.clicked.connect(self.show_import_export_page)

        # Start on entry page
        self.show_entry_page()

    # ---------------- Helper: placeholder page ----------------------
    def _make_placeholder_page(self, text: str) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        return page

    # ---------------- Page switchers --------------------------------
    def show_entry_page(self) -> None:
        self.stack.setCurrentWidget(self.entry_page)

    def show_entries_list_page(self) -> None:
        self.entries_list_page.load_entries()
        self.stack.setCurrentWidget(self.entries_list_page)

    def show_graphs_page(self) -> None:
        self.stack.setCurrentWidget(self.graphs_page)

    def show_import_export_page(self) -> None:
        self.stack.setCurrentWidget(self.import_export_page)

    # ---------------- Sidebar toggle --------------------------------
    def toggle_sidebar(self) -> None:
        """
        Show/hide the sidebar – the toggle button itself never disappears.
        """
        is_visible = self.sidebar_widget.isVisible()

        if is_visible:
            self.sidebar_widget.hide()
            self.menu_toggle_button.setText("Show Menu")
        else:
            self.sidebar_widget.show()
            self.menu_toggle_button.setText("Hide Menu")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
