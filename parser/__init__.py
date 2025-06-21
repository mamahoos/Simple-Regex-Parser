"""
This module provides functions to compile and match regex patterns using a custom NFA implementation.
"""

from regex_parser import RegexParser
from nfa_runner import NFARunner, MatchResult

def compile(pattern: str) -> NFARunner:
    """Compile a regex pattern into an NFARunner.
    This function takes a regex pattern as input, parses it into an NFA,

    Args:
        pattern (str): The regex pattern to compile.

    Returns:
        NFARunner: An NFARunner instance that can execute the NFA on input strings.
    """
    parser = RegexParser(pattern)
    nfa    = parser.parse()
    runner = NFARunner(nfa, parser.anchor_start, parser.anchor_end)
    return runner

def match(pattern: str, string: str) -> MatchResult | None:
    """Match a regex pattern against a string.
    
    This function compiles the regex pattern and checks if it matches the input string.

    Args:
        pattern (str): The regex pattern to match.
        string (str): The input string to check against the pattern.

    Returns:
        bool: True if the pattern matches the string, False otherwise.
    """
    runner = compile(pattern)
    return runner.match(string)

def search(pattern: str, string: str) -> MatchResult | None:
    """Search for a regex pattern in a string.
    
    This function compiles the regex pattern and searches for it in the input string.

    Args:
        pattern (str): The regex pattern to search for.
        string (str): The input string to search within.

    Returns:
        MatchResult | None: A MatchResult if a match is found, None otherwise.
    """
    runner = compile(pattern)
    return runner.search(string)