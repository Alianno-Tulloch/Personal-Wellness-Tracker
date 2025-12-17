import csv
file_path = 'data.csv'

# Note: Remember to add the CSV to the gitignore in the future, once the data testing is further along


"""
Writes data to a CSV file. Determines the format
"""
def write_to_csv(file_path, data_entry, mode = 'a'):
    with open(file_path, mode = mode, newline = '') as file:
        writer = csv.DictWriter(file, fieldnames = data_entry.keys())

        

"""
    Reads data from the CSV file, for use by other functions
    key = the specific column that's used to organize the data.
        by default, it's set to 'date'.
"""
def read_from_csv(file_path, key = 'date', mode = 'r'):

    # This version just outputs the data as a list of dictionaries in the terminal
    with open(file_path, mode = mode, newline = '') as file:
        reader = csv.DictReader(file)
        print("Data from the CSV:")
        for row in reader:
            print(row)
            print()


def main():
    # Example data entry
    data_entry = {
        "date": "2024-06-15",
        "hours_slept": 7.5,
        "exercise_minutes": 45,
        "mood_scale": 8,
        "mood_description": "happy",
        "activities": "jogging, reading, cooking",
        "notes": "Had a great day exploring new recipes and enjoying the sunshine. Felt energetic and positive throughout the day."
    }

    # Write the example data entry to CSV
    write_to_csv(file_path, data_entry)  # Use 'w' to create a new file or overwrite existing

    # Read and display data from CSV
    read_from_csv(file_path)

if __name__ == "__main__":
    main()