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
            # Check each language column and determine max pixel width based on suffix
            for lang, index in language_columns.items():
                text = row[index].strip()
                if not text:
                    error_message = (
                        f"Error in prefix '{prefix}' ({lang}): String is empty."
                    )
                    print(error_message)
                    error_messages.append(error_message)
                    row_passed = False
                else:
                    if prefix.endswith('_hint'):
                        max_pixel_width = 300
                    elif prefix.endswith('_name'):
                        max_pixel_width = 100
                    else:
                        max_pixel_width = 200  # Default maximum width
                    pixel_width = get_text_pixel_width(text, font_path, font_size)
                    if pixel_width > max_pixel_width:
                        error_message = (
                            f"Error in prefix '{prefix}' ({lang}), ({text}): Pixel width ({pixel_width}) exceeds {max_pixel_width}."
                        )
                        print(error_message)
                        error_messages.append(error_message)
                        row_passed = False
            if row_passed:
                rows_passed += 1
            else:
                rows_failed += 1
    print(f"Total rows checked: {rows_checked}")
    print(f"Rows passed: {rows_passed}")
    print(f"Rows failed: {rows_failed}")
    # Write summary output for GitHub Actions
    with open(os.environ['GITHUB_STEP_SUMMARY'], 'w') as summary_file:
        summary_file.write(f"## Summary of String and Pixel Length Checks\n")
        summary_file.write(f"- Total rows checked: {rows_checked}\n")
        summary_file.write(f"- :white_check_mark: Rows passed: {rows_passed}\n")
        summary_file.write(f"- :x: Rows failed: {rows_failed}\n")
        summary_file.write("\n### Errors:\n")
        for error_message in error_messages:
            summary_file.write(f"- {error_message}\n")
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_pixel_length.py <event_prefix>")
sys.exit(1)
    event_prefix = sys.argv[1]
    check_strings_and_pixel_length(event_prefix)
