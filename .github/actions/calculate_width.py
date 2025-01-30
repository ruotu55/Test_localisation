import sys

def calculate_width(input_string):
    width_summary = {}
    for char in input_string:
        char_width = len(char.encode('utf-8'))  # Calculate the width in bytes
        if char_width in width_summary:
            width_summary[char_width] += 1
        else:
            width_summary[char_width] = 1
    return width_summary

def main():
    if len(sys.argv) < 2:
        print("Usage: calculate_width.py <string>")
        sys.exit(1)

    input_string = sys.argv[1]
    width_summary = calculate_width(input_string)
    
    print("Character Width Summary:")
    for width, count in width_summary.items():
        print(f"Width {width}: {count} characters")

if __name__ == "__main__":
    main()
