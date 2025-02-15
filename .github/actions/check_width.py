import sys
import os
from PIL import ImageFont, ImageDraw, Image

def get_text_pixel_width(text, font_path='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', font_size=10):
    font = ImageFont.truetype(font_path, font_size)
    image = Image.new('RGB', (1, 1))
    draw = ImageDraw.Draw(image)
    bbox = draw.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0]
    return width

def visualize_text(text, font_path='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', font_size=10, image_file='text.png'):
    font = ImageFont.truetype(font_path, font_size)
    width = get_text_pixel_width(text, font_path, font_size)
    image = Image.new('RGB', (width + 10, font_size + 10), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.text((5, 5), text, font=font, fill=(0, 0, 0))
    image.save(image_file)
    print(f"Text visualized and saved as {image_file}")

def main():
    text_1 = "Ctdmm Xbffk Jxb"
    text_2 = "Qx Brf Nyrhryjua"
    
    font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'  # Path to the DejaVuSans truetype font file
    visualize_text(text_1, font_path=font_path, image_file='text_1.png')
    visualize_text(text_2, font_path=font_path, image_file='text_2.png')

if __name__ == "__main__":
    main()
