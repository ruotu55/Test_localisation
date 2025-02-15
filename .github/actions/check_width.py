import sys
import os
from PIL import ImageFont, ImageDraw, Image

def get_text_pixel_width(text, font_path, font_size):
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print(f"Font file '{font_path}' not found. Please make sure the font file is present in the directory or update the font path.")
        sys.exit(1)  # Exit if font not found to prevent further errors

    image = Image.new('RGB', (1, 1))
    draw = ImageDraw.Draw(image)
    width = draw.textsize(text, font=font)[0]
    return width

def main(event_name):
    font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'  # Path to the DejaVuSans truetype font file
    font_size = 10  # Font size

    try:
        words = event_name.split()
        word_widths = {word: get_text_pixel_width(word, font_path, font_size) for word in words}
        total_width_including_spaces = get_text_pixel_width(event_name, font_path, font_size)

        summary_text = f"The pixel width of the words and the total pixel width of the event name '{event_name}' including spaces is as follows:\n\n"
        for word, width in word_widths.items():
            summary_text += f"The pixel width of the word '{word}' is: {width}\n"
        summary_text += f"\nThe total pixel width of the event name '{event_name}' including spaces is: {total_width_including_spaces}\n"

        if 'GITHUB_STEP_SUMMARY' in os.environ: # Check if the environment variable exists
            with open(os.environ['GITHUB_STEP_SUMMARY'], 'w') as summary_file:
                summary_file.write(summary_text)

        print(summary_text)

    except Exception as e: # Catch any other exceptions
        print(f"An error occurred: {e}")
        sys.exit(1) # Exit with an error code

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_width.py <event_name>")
        sys.exit(1)
    event_name = sys.argv[1]
    main(event_name)
