import sys
import os
from PIL import ImageFont, ImageDraw, Image

def get_text_pixel_width(text, font_path, font_size=10):
    try:
        font = ImageFont.truetype(font_path, font_size)
    except OSError:
        print(f"Font file '{font_path}' not found. Please make sure the font file is present in the directory or update the font path.")
        return 0  # Return 0 if font is not found
    image = Image.new('RGB', (1, 1))
    draw = ImageDraw.Draw(image)
    bbox = draw.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0]
    return width

def main(event_name, font_path):
    font_size = 10
    try:
        words = event_name.split()
        word_widths = {word: get_text_pixel_width(word, font_path, font_size) for word in words}
        total_width_including_spaces = get_text_pixel_width(event_name, font_path, font_size)
        summary_text = f"The pixel width of the words and the total pixel width of the event name '{event_name}' including spaces is as follows:\n\n"
        for word, width in word_widths.items():
            summary_text += f"The pixel width of the word '{word}' is: {width}\n"
        summary_text += f"\nThe total pixel width of the event name '{event_name}' including spaces is: {total_width_including_spaces}\n"
        with open(os.environ['GITHUB_STEP_SUMMARY'], 'w') as summary_file:
            summary_file.write(summary_text)
        print(summary_text)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python check_width.py <event_name> <font_path>")
        sys.exit(1)
    event_name = sys.argv[1]
    font_path = sys.argv[2]
    main(event_name, font_path)
