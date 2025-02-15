import sys
import os
from PIL import ImageFont, ImageDraw

def get_text_pixel_width(text, font_path, font_size):
    font = ImageFont.truetype(font_path, font_size)
    image = Image.new('RGB', (1, 1))
    draw = ImageDraw.Draw(image)
    bbox = draw.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0]
    return width

def main(event_name):
    font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    font_size = 10
    try:
        words = event_name.split()
        word_widths = {word: get_text_pixel_width(word, font_path, font_size) for word in words}

        # Correctly calculate total width including spaces:
        total_width_including_spaces = 0
        for i, word in enumerate(words):
            total_width_including_spaces += word_widths[word]
            if i < len(words) - 1:  # Add space width if not the last word
                total_width_including_spaces += get_text_pixel_width(" ", font_path, font_size) # Width of space


        summary_text = f"The pixel width of the words and the total pixel width of the event name '{event_name}' including spaces is as follows:\n\n"
        for word, width in word_widths.items():
            summary_text += f"The pixel width of the word '{word}' is: {width}\n"
        summary_text += f"\nThe total pixel width of the event name '{event_name}' including spaces is: {total_width_including_spaces}\n"

        with open(os.environ.get('GITHUB_STEP_SUMMARY', 'summary.txt'), 'w') as summary_file: # Provide a default file name
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
