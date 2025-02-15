import sys
import os
from PIL import ImageFont, ImageDraw, Image

def get_text_pixel_width(text, font_path, font_size):
    font = ImageFont.truetype(font_path, font_size)
    image = Image.new('RGB', (2000, 50))  # Increased size! Important
    draw = ImageDraw.Draw(image)
    bbox = draw.textbbox((0, 0), text, font=font)
    cropped_image = image.crop(bbox)
    return cropped_image.size[0]

def main(event_name):
    font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    font_size = 10

    try:
        words = event_name.split()
        word_widths = {}

        # Iterate through words and calculate width *including* trailing space
        current_position = 0
        for i, word in enumerate(words):
            text_to_measure = word
            if i < len(words) - 1: # Add space if not the last word
                text_to_measure += " " # Add space after the word
            width = get_text_pixel_width(text_to_measure, font_path, font_size)
            word_widths[word] = width
            current_position += width

        total_width_including_spaces = get_text_pixel_width(event_name, font_path, font_size)


        summary_text = f"The pixel width of the words and the total pixel width of the event name '{event_name}' including spaces is as follows:\n\n"
        for word, width in word_widths.items():
            summary_text += f"The pixel width of the word '{word}' is: {width}\n"
        summary_text += f"\nThe total pixel width of the event name '{event_name}' including spaces is: {total_width_including_spaces}\n"

        with open(os.environ.get('GITHUB_STEP_SUMMARY', 'summary.txt'), 'w') as summary_file: # Default filename if env variable is not set
            summary_file.write(summary_text)

        print(summary_text)

    except IOError:
        print(f"Font file '{font_path}' not found. Please make sure the font file is present in the directory or update the font path.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_width.py <event_name>")
        sys.exit(1)
    event_name = sys.argv[1]
    main(event_name)
