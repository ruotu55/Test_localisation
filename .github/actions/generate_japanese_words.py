import random
import sys

hiragana = list("あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん")
katakana = list("アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン")
kanji = list("一二三四五上下左右中大小月火水木金土")

japanese_sets = hiragana + katakana + kanji

def generate_random_japanese_word(length):
    return ''.join(random.choice(japanese_sets) for _ in range(length))

if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            length = int(sys.argv[1])
        else:
            raise ValueError("No length provided")
        words = [generate_random_japanese_word(length) for _ in range(11)]
        print("Generated Japanese words:")
        for word in words:
            print(word)
    except ValueError:
        print("Invalid input. Please provide an integer.")
