import sys
from wcwidth import wcswidth

def get_display_width(s):
    return wcswidth(s)

def main(event_name):
    display_width = get_display_width(event_name)
    print(f"The display width of the event name '{event_name}' is: {display_width}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_width.py <event_name>")
        sys.exit(1)

    event_name = sys.argv[1]
    main(event_name)
