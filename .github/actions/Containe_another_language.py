import csv
import os
import sys
import re

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

# Initialize counters and error list
rows_checked = 0
rows_passed = 0
rows_failed = 0
error_messages = []

# Define character sets for each language (simplified for this example)
language_character_sets = {
    'English': re.compile(r'^[A-Za-z0-9 ]+$'),  # Only Latin characters, numbers, and spaces
    'Russian': re.compile(r'^[А-Яа-яЁё0-9 ]+$'),  # Only Cyrillic characters and numbers
    'French': re.compile(r'^[A-Za-zÀ-ÖØ-öø-ÿ0-9 ]+$'),  # Latin with French accents
    'German': re.compile(r'^[A-Za-zÄäÖöÜüß0-9 ]+$'),  # Latin with German characters
    'Spanish': re.compile(r'^[A-Za-zÁáÉéÍíÓóÚúÑñ0-9 ]+$'),  # Latin with Spanish accents
    'Italian': re.compile(r'^[A-Za-zÀ-ÖØ-öø-ÿ0-9 ]+$'),  # Latin with Italian accents
    'Japanese': re.compile(r'^[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF\uFF66-\uFF9F]+$'),  # Hiragana, Katakana, Kanji
    'Chinese (Simplified)': re.compile(r'^[\u4E00-\u9FFF]+$'),  # Simplified Chinese
    'Chinese (Traditional)': re.compile(r'^[\u4E00-\u9FFF]+$'),  # Traditional Chinese
    'Korean': re.compile(r'^[\uAC00-\uD7AF]+$'),  # Hangul characters
    'Portuguese': re.compile(r'^[A-Za-zÀ-ÖØ-öø-ÿ0-9 ]+$'),  # Latin with Portuguese accents
    'Thai': re.compile(r'^[\u0E00-\u0E7F]+$'),  # Thai characters
    'Turkish': re.compile(r'^[A-Za-zÇçĞğİıÖöŞşÜü0-9 ]+$'),  # Turkish letters
    'Indonesian': re.compile(r'^[A-Za-z0-9 ]+$'),  # Latin characters
    'Polish': re.compile(r'^[A-Za-zĄąĆćĘęŁłŃńÓóŚśŹźŻż0-9 ]+$'),  # Latin with Polish accents
}

# Function to check for invalid characters from other languages
def check_invalid_characters(event_prefix):
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

            row_passed = True
            rows_checked += 1

            # Check each language column for invalid characters
            for lang, index in language_columns.items():
                text = row[index].strip()
                if not text:
                    continue  # Skip empty text

                # Check if the text matches the expected character set for the language
                if not language_character_sets[lang].match(text):
                    error_message = (
                        f"Error in prefix '{prefix}' ({lang}): Contains invalid characters."
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
        summary_file.write(f"## Summary of Invalid Characters Check\n")
        summary_file.write(f"- Total rows checked: {rows_checked}\n")
        summary_file.write(f"- :white_check_mark: Rows passed: {rows_passed}\n")
        summary_file.write(f"- :x: Rows failed: {rows_failed}\n")
        summary_file.write("\n### Errors:\n")
        for error_message in error_messages:
            summary_file.write(f"- {error_message}\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_invalid_characters.py <event_prefix>")
        sys.exit(1)

    event_prefix = sys.argv[1]
    check_invalid_characters(event_prefix)
