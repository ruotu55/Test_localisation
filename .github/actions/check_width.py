import sys
import os
from PIL import ImageFont, ImageDraw, Image

def get_text_pixel_width(text, font_path, font_size=10):
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print(f"Font file '{font_path}' not found. Using default DejaVuSans")
        font_path_default = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
        font = ImageFont.truetype(font_path_default, font_size)

    total_width = 0
    for char in text:  # Iterate over each character
        image = Image.new('RGB', (1, 1))
        draw = ImageDraw.Draw(image)
        bbox = draw.textbbox((0, 0), char, font=font)
        width = bbox[2] - bbox[0]
        total_width += width
    return total_width


def main(event_name):
    event_name_upper = event_name.upper()
    font_path = "/usr/share/fonts/truetype/msttcorefonts/arial.ttf" # Likely path for Arial on Ubuntu after installing msttcorefonts
    font_size = 15

    try:
        words = event_name_upper.split()
        word_widths = {word: get_text_pixel_width(word, font_path, font_size) for word in words}
        total_width_including_spaces = get_text_pixel_width(event_name_upper, font_path, font_size)


        summary_text = f"The pixel width of the words and the total pixel width of the event name '{event_name_upper}' including spaces is as follows:\n\n"
        for word, width in word_widths.items():
            summary_text += f"The pixel width of the word '{word}' is: {width}\n"
        summary_text += f"\nThe total pixel width of the event name '{event_name_upper}' including spaces is: {total_width_including_spaces}\n"

        with open(os.environ['GITHUB_STEP_SUMMARY'], 'w') as summary_file:
            summary_file.write(summary_text)
        print(summary_text)

    except Exception as e: # Catching a broader exception for any issues
        print(f"An error occurred: {e}")
        print("Arial font may not be available. Using DejaVuSans as a fallback.")
        font_path_default = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
        words = event_name_upper.split()
        word_widths = {word: get_text_pixel_width(word, font_path_default, font_size) for word in words}
        total_width_including_spaces = get_text_pixel_width(event_name_upper, font_path_default, font_size)

        summary_text = f"The pixel width of the words and the total pixel width of the event name '{event_name_upper}' including spaces is as follows:\n\n"
        for word, width in word_widths.items():
            summary_text += f"The pixel width of the word '{word}' is: {width}\n"
        summary_text += f"\nThe total pixel width of the event name '{event_name_upper}' including spaces is: {total_width_including_spaces}\n"

        with open(os.environ['GITHUB_STEP_SUMMARY'], 'w') as summary_file:
            summary_file.write(summary_text)
        print(summary_text)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_width.py <event_name>")
        sys.exit(1)
    event_name = sys.argv[1]
    main(event_name)
