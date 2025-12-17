import csv
import os

def upsert_entry(file_path, data_entry):
    file_exists = os.path.isfile(file_path)