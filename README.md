# Personal Wellness Tracker

The Personal Wellness Tracker is a desktop app that helps you log your daily habits and mood, then view trends over time. You can record things like sleep, exercise, mood rating, mood tags, activities, and additional notes.

All the data is stored in a clean, structured way, so the data can later be visualized and analyzed.

This project is built using Python + PySide6, with CSV storage for now (SQLite planned later).

🖼️ Screenshots will go here later

# Inspiration for the Project

One day I spent the entire day gaming and felt miserable.
The next day, I spent the whole day learning French and felt amazing.

Lying in bed that night I thought:

    “I felt a lot better accomplishing the goals I set out for myself than I felt wasting an entire day playing video games.
    
    If only I had some way to empirically remind myself of that the next time I feel like doing nothing for a full day.”

So I started building a tool where I can:
- Track how I sleep, move, and feel
- Label my days with activities + tags
- Look back later and see patterns

The goal is to be able to look back on this and these stats, so I can be more honest to myself about how my choices affect my wellbeing.


## How It's Made:

**Tech Stack:** 
- Python
- PySide6 — desktop GUI
- pandas (planned for later) — data handling
- CSV storage (current) → SQLite (planned)

**Current Features**
- A Daily entry page with:
    - date (separate day / month / year inputs for accessibility)
    - sleep time (HH + MM)
    - exercise time (HH + MM)
    - mood scale (0.0 – 10.0)
    - mood tags (comma separated)
    - activities (comma separated)
    - optional notes field

- Form validation:
    - shows all errors at once
    - allows HH or MM to be blank as long as one is filled

- Data saved to a CSV file
- Entries update existing dates instead of duplicating them

## Project Structure

    /personal-wellness-tracker
    │
    ├── gui/                     # GUI pages (entry page, main menu, etc)
    ├── data_io.py               # read/write + upsert logic
    ├── data_validation.py       # field + entry validation
    ├── data_formatting.py       # HH:MM <-> minutes, date formatting, etc
    ├── data/entries.csv         # stored data
    └── README.md


## Future Plans

**Short-term**
- Add a Main Menu with multiple pages:
    - Daily Entry
    - Data Viewer (table view)
    - Graphs / Insights
    - Import / Export Data
- Improve visual styling & layout
- Add better error-display UX per-field

**Analytics & Graphing**
- Show mood vs sleep
- Show mood vs exercise
- Show frequency of tags / activities
- Show streaks or trendlines

**Storage Upgrade**
- Migrate from CSV → SQLite