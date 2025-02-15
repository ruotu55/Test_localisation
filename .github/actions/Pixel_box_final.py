import csv
import os
import sys
from PIL import ImageFont, ImageDraw, Image

csv_file = '.map-editor/locale/items.csv'
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

def get_text_pixel_width(text, font_path='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', font_size=10):
    font = ImageFont.truetype(font_path, font_size)
    image = Image.new('RGB', (1, 1))
    draw = ImageDraw.Draw(image)
    bbox = draw.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0]
    return width

def does_text_fit_in_two_lines(text, font_path='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', font_size=10, max_line_pixel_width=90):
    font = ImageFont.truetype(font_path, font_size)
    space_width = get_text_pixel_width(' ', font_path=font_path, font_size=font_size)
    lines = []
    current_line = []
    current_line_width = 0
    for word in text.split():
        word_width = get_text_pixel_width(word, font_path=font_path, font_size=font_size)
        if current_line_width + word_width + (space_width if current_line else 0) <= max_line_pixel_width:
            current_line.append(word)
            current_line_width += word_width + (space_width if current_line else 0)
        else:
            lines.append(current_line)
            current_line = [word]
            current_line_width = word_width
        if len(lines) + 1 > 2:  # As we only allow 2 lines
            return False

    lines.append(current_line)

    # Check for perfect fit on the second line and adjust space handling
    if len(lines) == 2:
        last_line_width = 0
        for w in lines[1]:
            last_line_width += get_text_pixel_width(w, font_path, font_size)
            if lines[1].index(w) < len(lines[1])-1:
                last_line_width += space_width

        first_line_width = 0
        for w in lines[0]:
            first_line_width += get_text_pixel_width(w, font_path, font_size)
            if lines[0].index(w) < len(lines[0])-1:
                first_line_width += space_width

        if first_line_width + last_line_width <= max_line_pixel_width*2:
            return True

    return len(lines) <= 2

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
            prefix = row[0]
            if not prefix.startswith(event_prefix):
                continue
            row_passed = True
            rows_checked += 1
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
                    if not does_text_fit_in_two_lines(text, font_path, font_size):
                        error_message = (
                            f"Error in prefix '{prefix}' ({lang}): Text exceeds 2 lines within pixel width limit. Text: '{text}'"
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
