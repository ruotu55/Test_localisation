import csv
import os
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

# Define maximum string lengths per language
language_max_lengths = {
    'Russian': {'name': 20, 'hint': 80},
    'English': {'name': 30, 'hint': 90},
    'French': {'name': 30, 'hint': 85},  # Placeholder value, can be changed later
    'German': {'name': 25, 'hint': 90},  # Placeholder value, can be changed later
    'Spanish': {'name': 28, 'hint': 95},  # Placeholder value, can be changed later
    'Italian': {'name': 22, 'hint': 88},  # Placeholder value, can be changed later
    'Japanese': {'name': 20, 'hint': 80},  # Placeholder value, can be changed later
    'Chinese (Simplified)': {'name': 25, 'hint': 85},  # Placeholder value, can be changed later
    'Korean': {'name': 23, 'hint': 90},  # Placeholder value, can be changed later
    'Portuguese': {'name': 30, 'hint': 95},  # Placeholder value, can be changed later
    'Thai': {'name': 25, 'hint': 85},  # Placeholder value, can be changed later
    'Turkish': {'name': 20, 'hint': 100},  # Placeholder value, can be changed later
    'Indonesian': {'name': 24, 'hint': 95},  # Placeholder value, can be changed later
    'Polish': {'name': 26, 'hint': 90},  # Placeholder value, can be changed later
    'Chinese (Traditional)': {'name': 20, 'hint': 80},  # Placeholder value, can be changed later
}

# Initialize counters and error list
rows_checked = 0
rows_passed = 0
rows_failed = 0
error_messages = []

# Function to check string lengths in each language column for each row
def check_string_length(event_prefix):
    global rows_checked, rows_passed, rows_failed
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # Skip rows that don't have enough columns
            if len(row) < 16:
                continue

            prefix = row[0]  # The prefix like '22120_tulips_i_flower_pink_name'
            if not prefix.startswith(event_prefix):
                continue

            # Determine whether this is a name or hint
            is_name = prefix.endswith('_name')
            row_passed = True
            rows_checked += 1

            # Check each language column
            for lang, index in language_columns.items():
                text = row[index].strip()
                max_length = language_max_lengths[lang]['name'] if is_name else language_max_lengths[lang]['hint']

                if len(text) > max_length:
                    error_message = (
                        f"Error in prefix '{prefix}' ({lang}): String is too long ({len(text)} characters): {text}"
                    )
                    print(error_message)
                    error_messages.append(error_message)
                    row_passed = False

            if row_passed:
                rows_passed += 1
            else:
                rows_failed += 1

    # Print summary at the end of the check
    print(f"Total rows checked: {rows_checked}")
    print(f"Rows passed: {rows_passed}")
    print(f"Rows failed: {rows_failed}")

    # Write summary output for GitHub Actions
    with open(os.environ['GITHUB_STEP_SUMMARY'], 'a') as summary_file:
        summary_file.write(f"## Summary of String Length Check\n")
        summary_file.write(f"- Total rows checked: {rows_checked}\n")
        summary_file.write(f"- :white_check_mark: Rows passed: {rows_passed}\n")
        summary_file.write(f"- :x: Rows failed: {rows_failed}\n")
        summary_file.write("\n### Errors:\n")
        for error_message in error_messages:
            summary_file.write(f"- {error_message}\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_csv.py <event_prefix>")
        sys.exit(1)

    event_prefix = sys.argv[1]
    check_string_length(event_prefix)
