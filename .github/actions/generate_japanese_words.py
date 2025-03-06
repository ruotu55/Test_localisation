# .github/actions/Pixel_box_final_generator.py
import random
import sys

# A more extensive Korean character list could be used
korean_characters = list("가나다라마바사아자차카타파하거너더러머버서어저처커터퍼허고노도로모보소오조초코토포호구누두루무부수우주추쿠투푸후그느드르므브스으즈츠크트프흐기니디리미비시이지치키티피히개내대래매배새애재채캐태패해게네데레메베세에제체케테페헤괴뇌되뢰뫼뵈쇠외죄최쾨퇴폐회")

def generate_random_korean_word(length):
    return ''.join(random.choice(korean_characters) for _ in range(length))

if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            length = int(sys.argv[1])
        else:
            raise ValueError("No length provided")
        words = [generate_random_korean_word(length) for _ in range(11)]
        print("Generated Korean words:")
        for word in words:
            print(word)
    except ValueError:
        print("Invalid input. Please provide an integer.")
