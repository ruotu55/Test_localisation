import unicodedata
import sys

def calculate_width(input_string):
    width = sum(unicodedata.east_asian_width(ch) in "WF" and 2 or 1 for ch in input_string)
    return width

if __name__ == "__main__":
    input_string = sys.argv[1]
    width = calculate_width(input_string)
    with open("width_output.txt", "w") as f:
        f.write(str(width))
