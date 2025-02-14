import sys
import os
from PIL import ImageFont, ImageDraw, Image

def get_text_pixel_width(text, font_path, font_size=10, first_letter_scale=1.2):
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print(f"Font file '{font_path}' not found. Using default DejaVuSans")
        font_path_default = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
        font = ImageFont.truetype(font_path_default, font_size)

    total_width = 0
    for char in text:
        image = Image.new('RGB', (1, 1))
        draw = ImageDraw.Draw(image)
        bbox = draw.textbbox((0, 0), char, font=font)
        width = bbox[2] - bbox[0]
        total_width += width
    return total_width


def main(event_name):
    font_path = "/usr/share/fonts/truetype/msttcorefonts/arial.ttf"  # Likely path for Arial on Ubuntu
    font_size = 10
    first_letter_scale = 1.2  # Scale factor for the first letter

    try:
        words = event_name.split()
        modified_words = []
        word_widths = {}
        total_width_including_spaces = 0

        for word in words:
            modified_word = ""
            first_char = word[0].upper()
            other_chars = word[1:].lower()
            modified_word = first_char + other_chars
            modified_words.append(modified_word)

            first_letter_width = get_text_pixel_width(first_char, font_path, int(font_size * first_letter_scale))
            rest_of_word_width = get_text_pixel_width(other_chars, font_path, font_size)

            word_width = first_letter_width + rest_of_word_width
            word_widths[modified_word] = word_width
            total_width_including_spaces += word_width

        total_width_including_spaces += get_text_pixel_width(" " * (len(words) -1 ), font_path, font_size) #add space width to total width

        modified_event_name = " ".join(modified_words)


        summary_text = f"The pixel width of the words and the total pixel width of the event name '{modified_event_name}' including spaces is as follows:\n\n"
        for word, width in word_widths.items():
            summary_text += f"The pixel width of the word '{word}' is: {width}\n"
        summary_text += f"\nThe total pixel width of the event name '{modified_event_name}' including spaces is: {total_width_including_spaces}\n"

        with open(os.environ['GITHUB_STEP_SUMMARY'], 'w') as summary_file:
            summary_file.write(summary_text)
        print(summary_text)

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Arial font may not be available. Using DejaVuSans as a fallback.")
        font_path_default = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
        words = event_name.split()
        modified_words = []
        word_widths = {}
        total_width_including_spaces = 0

        for word in words:
            modified_word = ""
            first_char = word[0].upper()
            other_chars = word[1:].lower()
            modified_word = first_char + other_chars
            modified_words.append(modified_word)

            first_letter_width = get_text_pixel_width(first_char, font_path_default, int(font_size * first_letter_scale))
            rest_of_word_width = get_text_pixel_width(other_chars, font_path_default, font_size)

            word_width = first_letter_width + rest_of_word_width
            word_widths[modified_word] = word_width
            total_width_including_spaces += word_width
        
        total_width_including_spaces += get_text_pixel_width(" " * (len(words) -1 ), font_path_default, font_size) #add space width to total width

        modified_event_name = " ".join(modified_words)

        summary_text = f"The pixel width of the words and the total pixel width of the event name '{modified_event_name}' including spaces is as follows:\n\n"
        for word, width in word_widths.items():
            summary_text += f"The pixel width of the word '{word}' is: {width}\n"
        summary_text += f"\nThe total pixel width of the event name '{modified_event_name}' including spaces is: {total_width_including_spaces}\n"

        with open(os.environ['GITHUB_STEP_SUMMARY'], 'w') as summary_file:
            summary_file.write(summary_text)
        print(summary_text)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_width.py <event_name>")
        sys.exit(1)
    event_name = sys.argv[1]
    main(event_name)
