# .github/actions/Pixel_box_final_generator.py
import random
import sys

chinese_characters = list("的一是不了人我在有他这来上大为和国地到以说时事要就出而可里后自都于之也家用能好下那年学起都就你我他她是谁很小么什么多少先生今天星期几号再见喜欢高兴漂亮") # A more extensive Chinese character list could be used

def generate_random_chinese_word(length):
    return ''.join(random.choice(chinese_characters) for _ in range(length))

if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            length = int(sys.argv[1])
        else:
            raise ValueError("No length provided")
        words = [generate_random_chinese_word(length) for _ in range(11)]
        print("Generated Chinese words:")
        for word in words:
            print(word)
    except ValueError:
        print("Invalid input. Please provide an integer.")
