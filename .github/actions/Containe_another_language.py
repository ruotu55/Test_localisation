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

# Linguistic family definitions based on writing scripts
linguistic_families = {
    'Indo-European': ['Russian', 'English', 'French', 'German', 'Spanish', 'Italian', 'Portuguese', 'Polish', 'Turkish'],
    'Sino-Tibetan': ['Chinese (Simplified)', 'Chinese (Traditional)'],
    'Japonic': ['Japanese'],
    'Koreanic': ['Korean'],
    'Austronesian': ['Indonesian', 'Thai']
}

# Initialize counters and error list
rows_checked = 0
rows_failed = 0
error_messages = []

# Function to check if one language's string contains another language's characters
def check_language_containment(event_prefix):
    global rows_checked, rows_failed
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # Skip rows that don't have enough columns
            if len(row) < 16:
                continue

            prefix = row[0]  # The prefix like '22120_tulips_i_flower_pink_name'
            if not prefix.startswith(event_prefix):
                continue

            rows_checked += 1
            row_failed = False

            # Get the text for each language and check families
            language_text = {lang: row[index].strip() for lang, index in language_columns.items()}

            # Check if one linguistic family's languages contain another linguistic family's characters
            for family1, languages1 in linguistic_families.items():
                for lang1 in languages1:
                    text1 = language_text.get(lang1, '')
                    for family2, languages2 in linguistic_families.items():
                        if family1 != family2:  # Don't compare languages in the same family
                            for lang2 in languages2:
                                text2 = language_text.get(lang2, '')
                                if text1 and text2:
                                    # Check if any character from lang2 is in lang1's string
                                    if any(c in text1 for c in text2):
                                        error_message = (
                                            f"Error in prefix '{prefix}': {lang2} contains characters from {lang1}."
                                        )
                                        print(error_message)
                                        error_messages.append(error_message)
                                        row_failed = True

            if row_failed:
                rows_failed += 1

    # Print summary at the end of the check
    print(f"Total rows checked: {rows_checked}")
    print(f"Rows failed: {rows_failed}")

    # Write summary output for GitHub Actions
    with open(os.environ['GITHUB_STEP_SUMMARY'], 'w') as summary_file:
        summary_file.write(f"## Summary of Language Containment Check\n")
        summary_file.write(f"- Total rows checked: {rows_checked}\n")
        summary_file.write(f"- :x: Rows failed: {rows_failed}\n")
        summary_file.write("\n### Errors:\n")
        for error_message in error_messages:
            summary_file.write(f"- {error_message}\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python Contain_another_language.py <event_prefix>")
        sys.exit(1)

    event_prefix = sys.argv[1]
    check_language_containment(event_prefix)
