import sys
from PIL import ImageFont, ImageDraw, Image

def get_text_pixel_width(text, font_path='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', font_size=10):
    # Use a truetype font
    font = ImageFont.truetype(font_path, font_size)
    # Create a dummy image and get the bounding box of the text
    image = Image.new('RGB', (1, 1))
    draw = ImageDraw.Draw(image)
    bbox = draw.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0]  # Calculate width from the bounding box
    return width

def main(event_name):
    font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'  # Path to the DejaVuSans truetype font file
    font_size = 10  # Font size
    try:
        words = event_name.split()

        # Calculate width for each word
        word_widths = {word: get_text_pixel_width(word, font_path, font_size) for word in words}
        total_width = sum(word_widths.values())

        # Print out the widths
        for word, width in word_widths.items():
            print(f"The pixel width of the word '{word}' is: {width}")
        
        print(f"\nThe total pixel width of the event name '{event_name}' is: {total_width}")
        
    except IOError:
        print(f"Font file '{font_path}' not found. Please make sure the font file is present in the directory or update the font path.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_width.py <event_name>")
        sys.exit(1)

    event_name = sys.argv[1]
    main(event_name)
