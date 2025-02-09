import csv
import os
import sys
from PIL import ImageFont, ImageDraw, Image
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
# Function to get the pixel width of the text using PIL
def get_text_pixel_width(text, font_path='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', font_size=10):
    font = ImageFont.truetype(font_path, font_size)
    image = Image.new('RGB', (1, 1))
    draw = ImageDraw.Draw(image)
    bbox = draw.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0]  # Calculate width from the bounding box
    return width
# Initialize counters and error list
rows_checked = 0
rows_passed = 0
rows_failed = 0
error_messages = []
def check_strings_and_pixel_length(event_prefix, font_path='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', font_size=10):
    global rows_checked, rows_passed, rows_failed
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) < 16:
                continue
            prefix = row[0]  # The prefix like '22120_tulips_i_flower_pink_name'
            if not prefix.startswith(event_prefix):
                continue
            row_passed = True
            rows_checked += 1
            # Check each language column
            for lang, index in language_columns.items():
                text = row[index].strip()
                if not text:
                    error_message = (
                        f"Error in prefix '{prefix}' ({lang}): String is empty."
                    )
                    error_messages.append(error_message)
                    row_passed = False
                else:
                    pixel_width = get_text_pixel_width(text, font_path, font_size)
                    if pixel_width > 200:
                        error_message = (
                            f"Error in prefix '{prefix}' ({lang}): Pixel width ({pixel_width}) exceeds 200."
                        )
                        error_messages.append(error_message)
                        row_passed = False
            if row_passed:
                rows_passed += 1
            else:
                rows_failed += 1
    summary = f"## Summary of String and Pixel Length Checks\n"
    summary += f"- Total rows checked: {rows_checked}\n"
    summary += f"- :white_check_mark: Rows passed: {rows_passed}\n"
    summary += f"- :x: Rows failed: {rows_failed}\n"
    summary += "\n### Errors:\n"
    for error_message in error_messages:
        summary += f"- {error_message}\n"
    # Write summary output for GitHub Actions
    summary_file_path = os.environ.get('GITHUB_STEP_SUMMARY', None)
    if summary_file_path:
        with open(summary_file_path, 'w') as summary_file:
            summary_file.write(summary)
    else:
print("GITHUB_STEP_SUMMARY environment variable is not set.")
        print(summary)
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_pixel_length.py <event_prefix>")
        sys.exit(1)
    event_prefix = sys.argv[1]
    check_strings_and_pixel_length(event_prefix)
