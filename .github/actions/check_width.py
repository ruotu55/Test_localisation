import sys
import os
from PIL import ImageFont, ImageDraw, Image
import unicodedata

def get_text_pixel_width(text, font_path, font_size=10):
    """Calculate the pixel width of the given text using the specified font."""
    # Normalize the text to ensure consistency
    text_normalized = unicodedata.normalize('NFC', text)
    
    # Load the TrueType font
    font = ImageFont.truetype(font_path, font_size)
    
    # Create a dummy image to get the bounding box of the text
    img = Image.new('RGB', (1, 1))
    draw = ImageDraw.Draw(img)
    bbox = draw.textbbox((0, 0), text_normalized, font=font)
    
    # Calculate and return the text width
    width = bbox[2] - bbox[0]
    return width

def main(event_name):
    font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    font_size = 10
    
    try:
        # Calculate width for the entire event name directly
        total_width_including_spaces = get_text_pixel_width(event_name, font_path, font_size)
        
        # Prepare and print the summary text
        summary_text = (
            f"The total pixel width of the event name '{event_name}' including spaces is: {total_width_including_spaces}\n"
        )
        
        # Write the summary to the file specified by GITHUB_STEP_SUMMARY
        github_summary_path = os.environ.get('GITHUB_STEP_SUMMARY')
        if github_summary_path:
            with open(github_summary_path, 'w') as summary_file:
                summary_file.write(summary_text)
        
        # Print summary to console
        print(summary_text)
    except IOError:
        print(f"Font file '{font_path}' not found. Please make sure the font file is present in the directory or update the font path.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_width.py <event_name>")
        sys.exit(1)
    
    event_name = sys.argv[1]
    main(event_name)
