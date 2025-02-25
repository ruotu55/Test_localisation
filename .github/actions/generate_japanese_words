import random

hiragana = list("あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん")
katakana = list("アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン")
kanji = list("一二三四五上下左右中大小月火水木金土")

japanese_sets = hiragana + katakana + kanji

def generate_random_japanese_word(length):
    return ''.join(random.choice(japanese_sets) for _ in range(length))

if __name__ == "__main__":
    try:
        length = int(input("Enter the desired length of the Japanese word: "))
        print(f"Generated Japanese word: {generate_random_japanese_word(length)}")
    except ValueError:
        print("Invalid input. Please enter an integer.")
