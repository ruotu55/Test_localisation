import os
import sys
import random
import string
from PIL import ImageFont, ImageDraw, Image

def get_text_pixel_width(text, font_path, font_size=10):
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print(f"Error: Could not load font file '{font_path}'.")
        return None
    image = Image.new('RGB', (1, 1))
    draw = ImageDraw.Draw(image)
    bbox = draw.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0]
    return width

def generate_word(font_path, font_size):
    letters = string.ascii_lowercase
    length = random.randint(1, 10)  # Vary the length of words
    word = ''.join(random.choice(letters) for _ in range(length))
    return word.capitalize()  # Capitalize the first letter of each word

def generate_sentence_with_width(desired_width, font_path, font_size, max_attempts=1000):
    space_width = get_text_pixel_width(' ', font_path, font_size)
    if space_width is None:
        return None
    for _ in range(max_attempts):
        num_words = random.randint(1, 3)
        words = [generate_word(font_path, font_size) for _ in range(num_words)]
        sentence = ' '.join(words)
        sentence_width = get_text_pixel_width(sentence, font_path, font_size)
        if sentence_width is None:
            return None
        if sentence_width == desired_width:
            return sentence
        elif sentence_width > desired_width:
            continue  # Skip sentences that are too long

    return None  # Return None if unable to find sentence of desired width within max_attempts

def main(desired_width, font_path):
    font_size = 10
    try:
        desired_width = int(desired_width)
        sentences = []
        for _ in range(50):
            sentence = generate_sentence_with_width(desired_width, font_path, font_size)
            if sentence:
                sentences.append(sentence)
            else:
                print(f"Unable to generate a sentence with width {desired_width} pixels.")
                break

        summary_text = f"Generated {len(sentences)} sentences with the width of {desired_width} pixels:\n\n"
        for sentence in sentences:
            summary_text += f"{sentence}\n"
        with open(os.environ['GITHUB_STEP_SUMMARY'], 'w') as summary_file:
            summary_file.write(summary_text)
        print(summary_text)
    except ValueError:
        print("Please provide a valid integer for the desired width.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python Pixel_box_final_generator.py <desired_width> <font_path>")
        sys.exit(1)
    desired_width = sys.argv[1]
    font_path = sys.argv[2]
    main(desired_width, font_path)
