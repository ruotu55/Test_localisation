import os
import sys
import random
from PIL import ImageFont, ImageDraw, Image

def get_text_pixel_width(text, font_path, font_size):
    font = ImageFont.truetype(font_path, font_size)
    image = Image.new('RGB', (1, 1))
    draw = ImageDraw.Draw(image)
    bbox = draw.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0]
    return width

def generate_word():
    # Set of Hiragana characters
    letters = 'あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん'
    length = random.randint(1, 10)  # Vary the length of words
    word = ''.join(random.choice(letters) for _ in range(length))
    return word  # Hiragana characters do not have capitalization

def generate_sentence_within_width_range(min_width, max_width, font_path, font_size, max_attempts=1000):
    for attempt in range(max_attempts):
        num_words = random.randint(1, 8)
        words = [generate_word() for _ in range(num_words)]
        sentence = ' '.join(words)
        sentence_width = get_text_pixel_width(sentence, font_path, font_size)
        
        # Debug print to check sentence width
        print(f"Attempt {attempt}: '{sentence}' (Width: {sentence_width}px)")
        
        if min_width <= sentence_width <= max_width:
            return sentence
    return None  # Return None if unable to find a sentence within width range within max_attempts

def main(min_width, max_width):
    font_path = '/usr/share/fonts/truetype/alegreya-sc/AlegreyaSansSC-Black.ttf'
    font_size = 10
    try:
        min_width = int(min_width)
        max_width = int(max_width)
        if min_width >= max_width:
            print("Minimum width should be less than the maximum width.")
            return

        sentences = []
        for _ in range(50):
            sentence = generate_sentence_within_width_range(min_width, max_width, font_path, font_size)
            if sentence:
                sentences.append(sentence)
            else:
                print(f"Unable to generate a sentence within width range {min_width}-{max_width} pixels.")
                break

        summary_text = f"Generated {len(sentences)} sentences within the width range of {min_width}-{max_width} pixels:\n\n"
        for sentence in sentences:
            summary_text += f"{sentence}\n"
        with open(os.environ.get('GITHUB_STEP_SUMMARY', 'summary.txt'), 'w') as summary_file:
            summary_file.write(summary_text)
        print(summary_text)
    except IOError:
        print(f"Font file '{font_path}' not found. Please make sure the font file is present in the directory or update the font path.")
    except ValueError:
        print("Please provide valid integers for the width range.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python Pixel_box_final_generator.py <min_width> <max_width>")
        sys.exit(1)
    min_width = sys.argv[1]
    max_width = sys.argv[2]
    main(min_width, max_width)
