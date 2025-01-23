import csv
import os
import sys
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0  # Seed the random number generator for reproducibility

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

# Group languages into broader categories
language_groups = {
    'European': ['en', 'fr', 'de', 'es', 'it', 'pt', 'pl'],
    'Asian': ['ja', 'ko', 'zh-cn', 'zh-tw', 'th'],
    'Slavic': ['ru'],
    'Turkic': ['tr'],
    'Austronesian': ['id']
}

# Map language to their group for lookup
lang_to_group = {}
for group, languages in language_groups.items():
    for lang in languages:
        lang_to_group[lang] = group

# Initialize counters and error list
rows_checked = 0
rows_passed = 0
rows_failed = 0
error_messages = []

# Function to check if strings are in the correct language group
def check_language_group(event_prefix):
    global rows_checked, rows_passed, rows_failed
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # Skip rows that don't have enough columns
            if len(row) < 16:
                continue

            prefix = row[0]
            if not prefix.startswith(event_prefix):
                continue

            rows_checked += 1
            row_passed = True

            for lang, index in language_columns.items():
                text = row[index].strip()
                if text:
                    detected_lang = detect(text)
                    detected_group = lang_to_group.get(detected_lang, 'Unknown')
                    # Map the display language to its group
                    expected_group = lang_to_group.get(lang.lower(), 'Unknown')

                    if detected_group != expected_group:
                        error_message = (
                            f"Error in prefix '{prefix}' ({lang}): Detected language group '{detected_group}' does not match expected group '{expected_group}'"
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
    with open(os.environ['GITHUB_STEP_SUMMARY'], 'w') as summary_file:
        summary_file.write(f"## Summary of Language Group Content Check\n")
        summary_file.write(f"- Total rows checked: {rows_checked}\n")
        summary_file.write(f"- :white_check_mark: Rows passed: {rows_passed}\n")
        summary_file.write(f"- :x: Rows failed: {rows_failed}\n")
        summary_file.write("\n### Errors:\n")
        for error_message in error_messages:
            summary_file.write(f"- {error_message}\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_language_content.py <event_prefix>")
        sys.exit(1)

    event_prefix = sys.argv[1]
    check_language_group(event_prefix)
