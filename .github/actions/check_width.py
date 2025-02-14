import sys
import os
from PIL import ImageFont, ImageDraw, Image
from langdetect import detect, DetectorFactory
# Ensure reproducibility of language detection
DetectorFactory.seed = 0
def get_text_pixel_width(text, font_path, font_size):
    # Use a truetype font
    font = ImageFont.truetype(font_path, font_size)
    # Create a dummy image and get the bounding box of the text
    image = Image.new('RGB', (1, 1))
    draw = ImageDraw.Draw(image)
    bbox = draw.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0]  # Calculate width from the bounding box
    return width
def detect_language(text):
    return detect(text)
def main(event_name, languages_font_sizes):
    font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'  # Path to the DejaVuSans truetype font file
    try:
        words = event_name.split()
        detected_language = detect_language(event_name)
        print(f"Detected language: {detected_language}")
        lang_code_to_name = {
            'ru': 'Russian',
            'en': 'English',
            'fr': 'French',
            'de': 'German',
            'es': 'Spanish',
            'it': 'Italian',
            'ja': 'Japanese',
            'zh-cn': 'Chinese (Simplified)',
            'ko': 'Korean',
            'pt': 'Portuguese',
            'th': 'Thai',
            'tr': 'Turkish',
            'id': 'Indonesian',
            'pl': 'Polish',
            'zh-tw': 'Chinese (Traditional)'
        }
        language = lang_code_to_name.get(detected_language, 'English')  # Default to English if undetected
        font_size = languages_font_sizes.get(language, 10)  # Default to font size 10
        # Calculate width for each word
        word_widths = {word: get_text_pixel_width(word, font_path, font_size) for word in words}
        # Calculate total width including spaces
        total_width_including_spaces = get_text_pixel_width(event_name, font_path, font_size)
        # Prepare the summary text
        summary_text = f"\nThe pixel width of the words and the total pixel width of the event name '{event_name}' in {language} (Font size: {font_size}) including spaces is as follows:\n\n"
        for word, width in word_widths.items():
            summary_text += f"The pixel width of the word '{word}' is: {width}\n"
        summary_text += f"\nThe total pixel width of the event name '{event_name}' in {language} including spaces is: {total_width_including_spaces}\n"
        # Write the summary to the file specified by GITHUB_STEP_SUMMARY
        with open(os.environ['GITHUB_STEP_SUMMARY'], 'w') as summary_file:
            summary_file.write(summary_text)
        # Print summary to console as well (optional)
        print(summary_text)
    except IOError:
        print(f"Font file '{font_path}' not found. Please make sure the font file is present in the directory or update the font path.")
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_width.py <event_name> [language:font_size]...")
        sys.exit(1)
    event_name = sys.argv[1]
    # Default font sizes for each language if not provided
    default_languages_font_sizes = {
        'Russian': 10,
        'English': 10,
        'French': 10,
        'German': 10,
        'Spanish': 10,
        'Italian': 10,
        'Japanese': 10,
        'Chinese (Simplified)': 10,
        'Korean': 10,
        'Portuguese': 10,
        'Thai': 10,
        'Turkish': 10,
        'Indonesian': 10,
        'Polish': 10,
        'Chinese (Traditional)': 10
    }
    languages_font_sizes = default_languages_font_sizes.copy()
    # Parse additional arguments if provided
    for arg in sys.argv[2:]:
        if ":" in arg:
            language, font_size = arg.split(":")
            if language in languages_font_sizes:
                languages_font_sizes[language] = int(font_size)
