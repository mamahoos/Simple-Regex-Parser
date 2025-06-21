from typing import cast, Tuple, Optional, Set
from nfa import TransitionLabel, State, NFA
from copy import deepcopy
import string


class RegexParser:
    r"""
    Parses a regular expression pattern and constructs the corresponding NFA.

    Supports:
        - Literals and escaped characters
        - Character classes ([abc], [a-z], [^a-z], etc.)
        - Quantifiers (*, +, ?, {n}, {n,}, {,m}, {n,m})
        - Alternation (|)
        - Grouping with parentheses
        - Anchors (^, $)
        - Dot (.) for wildcard
        - Shorthand character classes (\d, \w, \s)
    """

    def __init__(self, pattern: str):
        """
        Initialize the RegexParser with a pattern.

        Args:
            pattern (str): The regular expression pattern to parse.
        """
        self.pattern = pattern
        self.pos     = cast(int, 0)  # Current position in the pattern
        self.anchor_start: bool = False
        self.anchor_end  : bool = False

    def parse(self) -> NFA:
        """
        Parse the pattern and return the constructed NFA.

        Returns:
            NFA: The NFA representing the parsed regular expression.
        """
        if self._peek() == '^':
            self.anchor_start = True
            self._consume('^')

        nfa = self._expression()

        if self._peek() == '$':
            self.anchor_end = True
            self._consume('$')

        return nfa

    def _expression(self) -> NFA:
        """
        Parse an expression, handling alternation (|).

        Returns:
            NFA: The NFA for the parsed expression.
        """
        nfa = self._term()
        while self._peek() == '|':
            self._consume('|')
            nfa2 = self._term()
            nfa  = self._alternate(nfa, nfa2)
        return nfa

    def _term(self) -> NFA:
        """
        Parse a term, handling concatenation.

        Returns:
            NFA: The NFA for the parsed term.
        """
        nfa = self._factor()
        while (peek := self._peek()) and peek not in ')|':
            if peek == '$':
                break
            next_nfa = self._factor()
            nfa      = self._concatenate(nfa, next_nfa)
        return nfa

    def _factor(self) -> NFA:
        """
        Parse a factor, handling quantifiers (*, +, ?, {n}, etc).

        Returns:
            NFA: The NFA for the parsed factor.
        """
        nfa = self._base()
        while (peek := self._peek()) and peek in '*+?{':
            op = self._consume()
            match op:
                case '*':
                    nfa = self._kleene_star(nfa)
                case '+':
                    nfa = self._plus(nfa)
                case '?':
                    nfa = self._optional(nfa)
                case '{':
                    nfa = self._repeat(nfa)
                case _:
                    raise ValueError(f"Unexpected operator: {op}")

        return nfa

    def _base(self) -> NFA:
        """
        Parse a base element: group, escaped sequence, dot, character class, or literal.

        Returns:
            NFA: The NFA for the parsed base element.
        """
        char = self._peek()

        match char:

            case '(':
                self._consume('(')
                nfa = self._expression()
                self._consume(')')
                return nfa
            case '\\':
                self._consume('\\')
                escaped = self._consume()

                match escaped:
                    case 'd':
                        return self._digit()
                    case 'w':
                        return self._word()
                    case 's':
                        return self._space()
                    case _:
                        return self._literal(escaped)
            case '.':
                self._consume('.')
                return self._dot()
            case '[':
                self._consume('[')
                nfa = self._character_class()
                return nfa
            case _:
                return self._literal(self._consume())

    def _builtin_charset(self, key: str) -> set[str]:
        """
        Return the set of characters for a built-in character class.

        Args:
            key (str): The character class key ('d', 'w', 's', etc).

        Returns:
            set[str]: The set of characters for the class.
        """
        match key:
            case 'd':
                return set('0123456789')
            case 'w':
                return set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_')
            case 's':
                return set(' \t\r\n\f\v')
            case _:
                return set(key)  # fallback to literal character

    def _digit(self) -> NFA:
        """
        Construct an NFA that matches a single digit (0-9).

        Returns:
            NFA: The NFA for a digit.
        """
        start = State()
        end   = State()
        for c in self._builtin_charset('d'):
            symbol = TransitionLabel(c)
            start.add_transition(symbol, end)
        return NFA(start, end)

    def _word(self) -> NFA:
        """
        Construct an NFA that matches a word character (alphanumeric or underscore).

        Returns:
            NFA: The NFA for a word character.
        """
        start = State()
        end   = State()
        for c in self._builtin_charset('w'):
            symbol = TransitionLabel(c)
            start.add_transition(symbol, end)
        return NFA(start, end)

    def _space(self) -> NFA:
        """
        Construct an NFA that matches a whitespace character.

        Returns:
            NFA: The NFA for a whitespace character.
        """
        start = State()
        end   = State()
        for c in self._builtin_charset('s'):
            symbol = TransitionLabel(c)
            start.add_transition(symbol, end)
        return NFA(start, end)

    def _literal(self, char: str) -> NFA:
        """
        Construct an NFA that matches a single literal character.

        Args:
            char (str): The character to match.

        Returns:
            NFA: The NFA for the literal character.
        """
        start  = State()
        end    = State()
        symbol = TransitionLabel(char)
        start.add_transition(symbol, end)
        return NFA(start, end)

    def _concatenate(self, a: NFA, b: NFA) -> NFA:
        """
        Concatenate two NFAs.

        Args:
            a (NFA): The first NFA.
            b (NFA): The second NFA.

        Returns:
            NFA: The concatenated NFA.
        """
        epsilon = TransitionLabel(None)
        a.accept.add_transition(epsilon, b.start)
        return NFA(a.start, b.accept)

    def _alternate(self, a: NFA, b: NFA) -> NFA:
        """
        Create an NFA that matches either of two NFAs (alternation).

        Args:
            a (NFA): The first NFA.
            b (NFA): The second NFA.

        Returns:
            NFA: The alternation NFA.
        """
        start   = State()
        accept  = State()
        epsilon = TransitionLabel(None)
        start.add_transition(epsilon, a.start)
        start.add_transition(epsilon, b.start)
        a.accept.add_transition(epsilon, accept)
        b.accept.add_transition(epsilon, accept)
        return NFA(start, accept)

    def _kleene_star(self, a: NFA) -> NFA:
        """
        Apply the Kleene star (*) to an NFA.

        Args:
            a (NFA): The NFA to apply the star to.

        Returns:
            NFA: The resulting NFA.
        """
        start   = State()
        accept  = State()
        epsilon = TransitionLabel(None)
        start.add_transition(epsilon, a.start)
        start.add_transition(epsilon, accept)
        a.accept.add_transition(epsilon, a.start)
        a.accept.add_transition(epsilon, accept)
        return NFA(start, accept)

    def _plus(self, a: NFA) -> NFA:
        """
        Apply the plus quantifier (+) to an NFA.

        Args:
            a (NFA): The NFA to apply the plus to.

        Returns:
            NFA: The resulting NFA.
        """
        first = self._concatenate(a, self._kleene_star(a))
        return first

    def _optional(self, a: NFA) -> NFA:
        """
        Apply the optional quantifier (?) to an NFA.

        Args:
            a (NFA): The NFA to make optional.

        Returns:
            NFA: The resulting NFA.
        """
        start   = State()
        accept  = State()
        epsilon = TransitionLabel(None)
        start.add_transition(epsilon, a.start)
        start.add_transition(epsilon, accept)
        a.accept.add_transition(epsilon, accept)
        return NFA(start, accept)

    def _repeat(self, a: NFA) -> NFA:
        """
        Parse and apply the repeat quantifier {n}, {n,}, {,m}, or {n,m} to an NFA.

        Args:
            a (NFA): The base NFA to repeat.

        Returns:
            NFA: The repeated NFA.
        """
        min_repeats, max_repeats = self._parse_repeat_range()

        repeated = a
        for _ in range(min_repeats - 1):
            second   = self._clone_nfa(repeated)
            repeated = self._concatenate(repeated, second)

        if max_repeats is not None:
            for _ in range(max_repeats - min_repeats):
                second   = self._optional(self._clone_nfa(repeated))
                repeated = self._concatenate(repeated, second)
        else:
            second   = self._kleene_star(self._clone_nfa(a))
            repeated = self._concatenate(repeated, second)

        return repeated

    def _parse_repeat_range(self) -> Tuple[int, Optional[int]]:
        """
        Parse the contents inside { and } to determine the repeat range.

        Returns:
            Tuple[int, Optional[int]]: (min_repeats, max_repeats) where max_repeats can be None for unbounded.
        """
        num_string = ''
        min_value  = 0
        max_value  = None
        char       = self._peek()

        if char == ',':
            self._consume(',')
        else:
            while (peek := self._peek()) and peek.isdigit():
                num_string += self._consume()
            min_value = int(num_string) if num_string else 0

            if self._peek() == ',':
                self._consume(',')
            else:
                self._consume('}')
                return (min_value, max_value)   # Exact repeat {n}

        num_string = ''
        while (peek := self._peek()) and peek.isdigit():
            num_string += self._consume()

        if num_string:
            max_value = int(num_string)

        self._consume('}')
        return (min_value, max_value)

    def _clone_nfa(self, nfa: NFA) -> NFA:
        """
        Create a deep copy of the given NFA.

        Args:
            nfa (NFA): The NFA to clone.

        Returns:
            NFA: A deep copy of the NFA.
        """
        return deepcopy(nfa)

    def _dot(self) -> NFA:
        """
        Construct an NFA that matches any single character.

        Returns:
            NFA: The NFA for any character.
        """
        start = State()
        end   = State()
        dot   = TransitionLabel('.', is_wildcard=True)
        start.add_transition(dot, end)
        return NFA(start, end)

    def _character_class(self) -> NFA:
        """
        Parse and construct an NFA that matches a character class.

        Supports positive and negative character classes, character ranges (a-z), and escaped characters.

        Returns:
            NFA: The NFA for the character class.
        """
        start  = State()
        end    = State()
        chars  = cast(Set[str], set())
        negate = False

        if self._peek() == '^':
            negate = True
            self._consume('^')

        while (peek := self._peek()) and peek != ']':
            if peek == '\\':
                self._consume('\\')
                escaped = self._consume()
                chars.update(self._builtin_charset(escaped))
            elif peek and self.pos + 2 < len(self.pattern) and self.pattern[self.pos + 1] == '-':
                start_ch = self._consume()
                self._consume('-')
                end_ch   = self._consume()
                chars.update(chr(c) for c in range(ord(start_ch), ord(end_ch) + 1))
            else:
                chars.add(self._consume())

        self._consume(']')

        if negate:
            universe = set(string.printable)
            chars    = universe - chars

        for char in chars:
            symbol = TransitionLabel(char, is_wildcard=False)
            start.add_transition(symbol, end)

        return NFA(start, end)

    def _peek(self) -> Optional[str]:
        """
        Return the next character in the pattern without consuming it.

        Returns:
            Optional[str]: The next character, or None if at the end.
        """
        return self.pattern[self.pos] if self.pos < len(self.pattern) else None

    def _consume(self, expected: Optional[str] = None) -> str:
        """
        Consume and return the next character in the pattern.

        Args:
            expected (Optional[str]): If provided, raises an error if the next character does not match.

        Returns:
            str: The consumed character.

        Raises:
            ValueError: If the end of the pattern is reached or the expected character does not match.
        """
        if self.pos >= len(self.pattern):
            raise ValueError(f"Unexpected end of pattern. Expected {ascii(expected)}")
        char = self.pattern[self.pos]
        if expected and char != expected:
            raise ValueError(f"Expected {ascii(expected)} but got {ascii(char)} at index {self.pos}")
        self.pos += 1
        return char