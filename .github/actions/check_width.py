import sys
from PIL import ImageFont, ImageDraw, Image

def get_text_pixel_width(text, font_path='arial.ttf', font_size=12):
    # Use a truetype font
    font = ImageFont.truetype(font_path, font_size)
    # Create a dummy image and get the size of the text
    image = Image.new('RGB', (1, 1))
    draw = ImageDraw.Draw(image)
    width, _ = draw.textsize(text, font=font)
    return width

def main(event_name):
    font_path = 'arial.ttf'  # Path to the ttf font file
    font_size = 12  # Font size
    try:
        display_width = get_text_pixel_width(event_name, font_path, font_size)
        print(f"The pixel width of the event name '{event_name}' is: {display_width}")
    except IOError:
        print(f"Font file '{font_path}' not found. Please make sure the font file is present in the directory.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_width.py <event_name>")
        sys.exit(1)

    event_name = sys.argv[1]
    main(event_name)
