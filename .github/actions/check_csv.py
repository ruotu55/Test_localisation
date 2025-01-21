import csv
import os

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

# Initialize counters for passed rows
rows_checked = 0
rows_passed = 0
rows_failed = 0

# Function to check the string lengths in each language column for each row
def check_string_length():
    global rows_checked, rows_passed, rows_failed
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # Skip rows that don't have enough columns
            if len(row) < 16:
                continue

            prefix = row[0]  # The prefix like '22120_tulips_i_flower_pink_name'
            row_passed = True
            rows_checked += 1

            # Check each language column
            for lang, index in language_columns.items():
                text = row[index].strip()
                if len(text) > 10:
                    # Print detailed error with prefix, language, and string
                    print(f"Error in prefix '{prefix}' ({lang}): String is too long ({len(text)} characters): {text}")
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
        summary_file.write(f"- ✅ Rows passed: {rows_passed}\n")
        summary_file.write(f"- ❌ Rows failed: {rows_failed}\n")

if __name__ == "__main__":
    check_string_length()
