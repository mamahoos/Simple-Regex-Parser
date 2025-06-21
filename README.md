# SimpleRegexParser
A minimal Python library for parsing and simulating regular expressions using nondeterministic finite automata (NFA).  
SimpleRegexParser is designed for educational purposes, providing a clear and modular implementation of regex parsing, AST generation, and NFA simulation.

---
## Overview

SimpleRegexParser is a pure Python library that parses standard regular expressions and simulates their matching using nondeterministic finite automata (NFA). It is designed for clarity and educational value, focusing on the core mechanics of regex parsing and NFA execution without external dependencies.

---

## Core Components

- **NFA Construction:**  
    The `nfa.py` module defines the `TransitionLabel`, `State`, and `NFA` classes, providing the foundation for building and representing NFAs. Each regex pattern is compiled into an NFA, which models all possible matching paths.

- **Regex Parsing:**  
    The `regex_parser.py` module implements the `RegexParser` class, which parses regex patterns (including literals, character classes, quantifiers, alternation, grouping, anchors, dot, and shorthand classes) and constructs the corresponding NFA.

- **NFA Simulation:**  
    The `nfa_runner.py` module provides the `NFARunner` and `MatchResult` classes. `NFARunner` executes the NFA on input strings, supporting matching, searching, and finding all matches, with support for anchors and wildcards.

- **API Functions:**  
    The `__init__.py` file exposes a simple API:
    - `compile(pattern: str) -> NFARunner`: Compiles a regex pattern into an NFA runner.
    - `match(pattern: str, string: str) -> MatchResult | None`: Checks if the entire string matches the pattern.
    - `search(pattern: str, string: str) -> MatchResult | None`: Searches for the pattern anywhere in the string.

---

## Example

```python
from parser import compile, match, search

runner = compile(r"a(b|c)*d")
result = runner.match("abcbcd")
if result:
        print("Matched:", result.group())
else:
        print("No match.")

# Or use the convenience function:
if match(r"a(b|c)*d", "abcbcd"):
        print("Full match!")
```

---

## Supported Regex Features

- Literals and escaped characters
- Character classes: `[abc]`, `[a-z]`, `[^a-z]`
- Quantifiers: `*`, `+`, `?`, `{n}`, `{n,}`, `{,m}`, `{n,m}`
- Alternation: `|`
- Grouping: `(...)`
- Anchors: `^`, `$`
- Dot (`.`) wildcard
- Shorthand classes: `\d`, `\w`, `\s`

---

## Limitations

- No support for lookahead/lookbehind, named groups, or advanced flags
- No Unicode or locale-specific features
- No DFA optimization (pure NFA simulation)

---

## Features

- Parse standard regular expressions into an abstract syntax tree (AST)
- Convert regex ASTs into NFAs for pattern matching
- Simulate NFA execution to test string matches
- Modular, well-documented codebase for easy understanding and extension

---

SimpleRegexParser is ideal for students, educators, and anyone interested in learning how regular expressions work under the hood.

## Project Structure

```
parser/
├── nfa.py           # Core NFA construction and simulation logic
├── regex_parser.py  # Regex pattern parsing and AST generation
├── tokens.py        # Token definitions for regex parsing
├── utils.py         # Utility functions
└── __init__.py      # Package initialization
```

- **nfa.py:** Implements the NFA data structures and algorithms for simulating regex matches.
- **regex_parser.py:** Parses regex patterns into an abstract syntax tree (AST) and translates them into NFA.
- **tokens.py:** Defines token types and helpers for the regex parser.
- **utils.py:** Contains helper functions used throughout the project.

---

## Usage

1. **Clone the repository:**
    ```sh
    git clone https://github.com/mamahoos/SimpleRegexParser.git
    cd SimpleRegexParser
    ```

2. **Run a sample:**
    ```sh
    python -m parser.regex_parser "a(b|c)*d" "abcbcd"
    ```
    Adjust the command as needed for your environment and test cases.

3. **Integrate in your code:**
    Import the relevant modules from `parser/` and use the provided classes and functions to parse and match regex patterns.

---

## How It Works

- The regex pattern is parsed into tokens and then into an AST.
- The AST is converted into an NFA.
- The NFA is simulated to match input strings.

This approach helps visualize and understand how regular expressions are processed internally.

---

## TODO

- [ ] Add lookahead and lookbehind support
- [ ] Implement NFA optimizer for performance improvements
- [ ] Add regex flags (e.g., case-insensitive, multiline)
- [ ] Expand regex feature set (e.g., Unicode support)
- [ ] Improve error handling and reporting
- [ ] Add more comprehensive tests and examples

---

## License

It's a simple project for educational purposes.

---

## Acknowledgements

Inspired by academic materials from the Theory of Languages and Automata course.


