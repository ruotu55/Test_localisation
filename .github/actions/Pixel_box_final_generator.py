# .github/actions/Pixel_box_final_generator.py
import random
import sys

portuguese_characters = list("abcdefghijklmnopqrstuvwxyzáéíóúçãõâêîôûàèìòù")  # A more extensive Portuguese character list could be used

def generate_random_portuguese_word(length):
    return ''.join(random.choice(portuguese_characters) for _ in range(length))

if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            length = int(sys.argv[1])
        else:
            raise ValueError("No length provided")
        words = [generate_random_portuguese_word(length) for _ in range(11)]
        print("Generated Portuguese words:")
        for word in words:
            print(word)
    except ValueError:
        print("Invalid input. Please provide an integer.")
