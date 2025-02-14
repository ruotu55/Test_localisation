import os
import sys
import random
import string
from PIL import ImageFont, ImageDraw, Image

def get_text_pixel_width(text, font_path='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', font_size=10):
    font = ImageFont.truetype(font_path, font_size)
    image = Image.new('RGB', (1, 1))
    draw = ImageDraw.Draw(image)
    bbox = draw.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0]
    return width

def generate_random_word_with_width(desired_width, font_path, font_size, max_attempts=1000):
    letters = string.ascii_lowercase
    avg_char_width = get_text_pixel_width('a', font_path, font_size)
    approx_length = desired_width // avg_char_width

    for _ in range(max_attempts):
        word = ''.join(random.choice(letters) for _ in range(approx_length))
        word_width = get_text_pixel_width(word, font_path, font_size)
        if word_width == desired_width:
            return word
        elif word_width > desired_width:
            reduced_length = int(len(word) * desired_width / word_width)
            word = word[:reduced_length]
            if get_text_pixel_width(word, font_path, font_size) == desired_width:
                return word
    
    return None  # Return None if unable to find word of desired width within max_attempts

def main(desired_width):
    font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    font_size = 10
    try:
        desired_width = int(desired_width)
        words = []
        for _ in range(50):
            word = generate_random_word_with_width(desired_width, font_path, font_size)
            if word:
                words.append(word)
            else:
                print(f"Unable to generate a word with width {desired_width} pixels.")
                break
        
        summary_text = f"Generated {len(words)} words with the width of {desired_width} pixels:\n\n"
        for word in words:
            summary_text += f"{word}\n"
        with open(os.environ['GITHUB_STEP_SUMMARY'], 'w') as summary_file:
            summary_file.write(summary_text)
        print(summary_text)
    except IOError:
        print(f"Font file '{font_path}' not found. Please make sure the font file is present in the directory or update the font path.")
    except ValueError:
        print("Please provide a valid integer for the desired width.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python Pixel_box_final_generator.py <desired_width>")
        sys.exit(1)
    desired_width = sys.argv[1]
    main(desired_width)
