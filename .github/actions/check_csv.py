import csv
import sys
import os  # Make sure to import the os module

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

# Initialize counters for passed and failed strings
total_checked = 0
total_passed = 0
total_failed = 0

# Function to check the string lengths in each language column
def check_string_length():
    global total_checked, total_passed, total_failed
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # Skip rows that don't have enough columns
            if len(row) < 16:
                continue

            for lang, index in language_columns.items():
                text = row[index].strip()
                total_checked += 1
                if len(text) <= 10:
                    total_passed += 1
                else:
                    print(f"Error: String in {lang} is too long ({len(text)} characters): {text}")
                    total_failed += 1

    # Print summary at the end of the check
    print(f"Total strings checked: {total_checked}")
    print(f"Total strings passed: {total_passed}")
    print(f"Total strings failed: {total_failed}")

    # Write summary output for GitHub Actions
    with open(os.environ['GITHUB_STEP_SUMMARY'], 'a') as summary_file:
        summary_file.write(f"## Summary of String Length Check\n")
        summary_file.write(f"- Total strings checked: {total_checked}\n")
        summary_file.write(f"- ✅ Strings passed: {total_passed}\n")
        summary_file.write(f"- ❌ Strings failed: {total_failed}\n")

    # Exit with an error code if any strings failed
    if total_failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    check_string_length()
