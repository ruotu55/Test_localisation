import sys
from wcwidth import wcwidth

def calculate_width(input_string):
    total_width = 0
    for char in input_string:
        char_width = wcwidth(char)
        if char_width == -1:
            print(f"Warning: Character {char} is not printable, skipping.")
            continue
        total_width += char_width
    return total_width

def main():
    if len(sys.argv) < 2:
        print("Usage: calculate_width.py <string>")
        sys.exit(1)

    input_string = sys.argv[1]
    total_width = calculate_width(input_string)
    
    print(f"Total visual width of the string is: {total_width} columns")

if __name__ == "__main__":
    main()
