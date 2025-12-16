import csv
file_path = 'data.csv'


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
