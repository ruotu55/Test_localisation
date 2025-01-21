import csv
import sys

# Path to the CSV file relative to the repository root
csv_file = '.map-editor/locale/items.csv'

# Define the indices of the languages in the CSV file
language_columns = {
    'Russian': 1,
    'English': 2,
    'French': 3,
    'German': 4,
    'Spanish': 5,
    'Italian': 6,
    'Japanese': 7,
    'Chinese (Simplified)': 8,
    'Korean': 9,
    'Portuguese': 10,
    'Thai': 11,
    'Turkish': 12,
    'Indonesian': 13,
    'Polish': 14,
    'Chinese (Traditional)': 15
}

# Function to check the string lengths in each language column
def check_string_length():
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # Skip rows that don't have enough columns
            if len(row) < 16:
                continue

            for lang, index in language_columns.items():
                text = row[index].strip()
                if len(text) > 10:
                    print(f"Error: String in {lang} is too long ({len(text)} characters): {text}")
                    sys.exit(1)

    print("All strings are within the allowed length.")

if __name__
