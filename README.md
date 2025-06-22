# SimpleRegexParser
A minimal Python library for parsing and simulating regular expressions using nondeterministic finite automata (NFA).  
SimpleRegexParser is designed for educational purposes, providing a clear and modular implementation of regex parsing, AST generation, and NFA simulation.

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

## Project Structure

```
nfa_regex/
├── __main__.py        # Entry point for command-line usage: allows running regex matching from the terminal
├── __init__.py        # Public API: compile, match, search
├── nfa.py             # Core NFA data structures and transitions
├── regex_parser.py    # Regex pattern parser and NFA builder
├── nfa_runner.py      # NFA simulation and matching engine
```

---

## Usage

1. **Clone the repository:**
    ```sh
    git clone https://github.com/mamahoos/SimpleRegexParser.git
    cd SimpleRegexParser
    ```

2. **Import and use in your Python code:**
    ```python
    from nfa_regex import compile, match, search

    runner = compile("abc")
    print(runner.match("abc"))      # Full match
    print(runner.match("ab"))       # None (no match)
    print(search("a.c", "xxabcxx")) # Finds 'abc' in the string
    ```

3. **Command-line usage:**

    You can also run regex matching directly from the terminal:
    ```sh
    python -m nfa_regex "<pattern>" "<string>"
    ```
    Example:
    ```sh
    python -m nfa_regex "a(b|c)*d" "abcbcd"
    ```

    If a match is found, the matched result will be printed; otherwise, you will see `No match

---

## License

This project is licensed under the [MIT License](LICENSE).


