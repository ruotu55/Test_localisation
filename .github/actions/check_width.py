import sys
import os
from PIL import ImageFont, ImageDraw, Image

def get_text_pixel_width(text, font_path='/usr/share/fonts/truetype/alegreya-sc/AlegreyaSansSC-Black.ttf', font_size=10):
    # Use a truetype font
    font = ImageFont.truetype(font_path, font_size)
    # Create a dummy image and get the bounding box of the text
    image = Image.new('RGB', (1, 1))
    draw = ImageDraw.Draw(image)
    bbox = draw.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0]  # Calculate width from the bounding box
    return width

def main(event_name):
    font_path = '/usr/share/fonts/truetype/alegreya-sc/AlegreyaSansSC-Black.ttf'  # Path to the AlegreyaSC-Black truetype font file
    font_size = 10  # Font size
    try:
        words = event_name.split()
        # Calculate width for each word
        word_widths = {word: get_text_pixel_width(word, font_path, font_size) for word in words}
        # Calculate total width including spaces
        total_width_including_spaces = get_text_pixel_width(event_name, font_path, font_size)
        # Prepare the summary text
        summary_text = f"The pixel width of the words and the total pixel width of the event name '{event_name}' including spaces is as follows:\n\n"
        for word, width in word_widths.items():
            summary_text += f"The pixel width of the word '{word}' is: {width}\n"
        summary_text += f"\nThe total pixel width of the event name '{event_name}' including spaces is: {total_width_including_spaces}\n" # Corrected Line
        # Write the summary to the file specified by GITHUB_STEP_SUMMARY
        with open(os.environ['GITHUB_STEP_SUMMARY'], 'w') as summary_file:
            summary_file.write(summary_text)
        # Print summary to console as well (optional)
        print(summary_text)
    except IOError:
        print(f"Font file '{font_path}' not found. Please make sure the font file is present in the directory or update the font path.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_width.py <event_name>")
        sys.exit(1)
    event_name = sys.argv[1]
    main(event_name)
