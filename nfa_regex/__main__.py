from . import match
import sys

def main() -> None:
    """
    Main function to run the NFA regex matching from the command line.
    """
    if len(sys.argv) != 3:
        print("Usage: python -m nfa_regex <regex> <string>")
        sys.exit(1)

    regex  = sys.argv[1]
    string = sys.argv[2]

    if (result := match(regex, string)):
        print(result)
    else:
        print("No match found.")
    