# .github/actions/Pixel_box_final_generator.py
import random
import sys

# เพิ่มรายการตัวอักษรภาษาไทยที่ครอบคลุม
thai_characters = list("กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬอฮะัาำิีึืุูเแโใไ่้๊๋ฯๆ์ํ็่้​")

def generate_random_thai_word(length):
    return ''.join(random.choice(thai_characters) for _ in range(length))

if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            length = int(sys.argv[1])
        else:
            raise ValueError("No length provided")
        words = [generate_random_thai_word(length) for _ in range(11)]
        print("Generated Thai words:")
        for word in words:
            print(word)
    except ValueError:
        print("Invalid input. Please provide an integer.")
