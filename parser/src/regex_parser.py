from nfa import TransitionLabel, State, NFA
from typing import cast, Tuple, Optional
from copy import deepcopy


class RegexParser:
    r"""
    Parses a regular expression pattern and constructs the corresponding NFA.
    Supports basic regex features: ., *, +, ?, |, (), ^, $, \d, \w, \s, and escaped literals.
    """
    
    def __init__(self, pattern: str):
        """
        Initializes the parser with the given pattern.

        ### Args:
            pattern (str): The regular expression pattern to parse.
        """
        self.pattern = pattern
        self.pos     = cast(int, 0)  # Current position in the pattern
        self.anchor_start: bool = False
        self.anchor_end  : bool = False

    def parse(self) -> NFA:
        """
        Parses the pattern and returns the constructed NFA.

        ### Returns:
            NFA: The NFA representing the parsed regular expression.
        """
        # Step 1
        if self._peek() == '^':
            self.anchor_start = True
            self._consume('^')
            
        # Step 2
        nfa = self._expression()
        
        # Step 3
        if self._peek() == '$':
            self.anchor_end = True
            self._consume('$')
            
        return nfa

    def _expression(self) -> NFA:
        """
        Parses an expression, handling alternation (|).

        ### Returns:
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
        Parses a term, handling concatenation.

        ### Returns:
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
        Parses a factor, handling quantifiers (*, +, ?).

        ### Returns:
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
        Parses a base element: group, escaped sequence, dot, or literal.

        ### Returns:
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
                self._consume(']')
                return nfa
            case _:
                return self._literal(self._consume())

    def _digit(self) -> NFA:
        """
        Constructs an NFA that matches a single digit (0-9).

        ### Returns:
            NFA: The NFA for a digit.
        """
        start = State()
        end   = State()
        for c in '0123456789':
            symbol = TransitionLabel(c)
            start.add_transition(symbol, end)
        return NFA(start, end)

    def _word(self) -> NFA:
        """
        Constructs an NFA that matches a word character (alphanumeric or underscore).

        ### Returns:
            NFA: The NFA for a word character.
        """
        start = State()
        end   = State()
        for c in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_':
            symbol = TransitionLabel(c)
            start.add_transition(symbol, end)
        return NFA(start, end)

    def _space(self) -> NFA:
        """
        Constructs an NFA that matches a whitespace character.

        ### Returns:
            NFA: The NFA for a whitespace character.
        """
        start = State()
        end   = State()
        for c in ' \t\r\n\f\v':
            symbol = TransitionLabel(c)
            start.add_transition(symbol, end)
        return NFA(start, end)

    def _literal(self, char: str) -> NFA:
        """
        Constructs an NFA that matches a single literal character.

        ### Args:
            char (str): The character to match.

        ### Returns:
            NFA: The NFA for the literal character.
        """
        start  = State()
        end    = State()
        symbol = TransitionLabel(char)
        start.add_transition(symbol, end)
        return NFA(start, end)

    def _concatenate(self, a: NFA, b: NFA) -> NFA:
        """
        Concatenates two NFAs.

        ### Args:
            a (NFA): The first NFA.
            b (NFA): The second NFA.

        ### Returns:
            NFA: The concatenated NFA.
        """
        epsilon = TransitionLabel(None)
        a.accept.add_transition(epsilon, b.start)
        return NFA(a.start, b.accept)
    

    def _alternate(self, a: NFA, b: NFA) -> NFA:
        """
        Creates an NFA that matches either of two NFAs (alternation).

        ### Args:
            a (NFA): The first NFA.
            b (NFA): The second NFA.

        ### Returns:
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
        Applies the Kleene star (*) to an NFA.

        ### Args:
            a (NFA): The NFA to apply the star to.

        ### Returns:
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
        Applies the plus quantifier (+) to an NFA.

        ### Args:
            a (NFA): The NFA to apply the plus to.

        ### Returns:
            NFA: The resulting NFA.
        """
        first = self._concatenate(a, self._kleene_star(a))
        return first

    def _optional(self, a: NFA) -> NFA:
        """
        Applies the optional quantifier (?) to an NFA.

        ### Args:
            a (NFA): The NFA to make optional.

        ### Returns:
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
        """Parses and applies the repeat quantifier {n}, {n,}, {,m}, or {n,m} to an NFA.

        ### Args:
            a (NFA): the base NFA to repeat.

        ### Returns:
            NFA: The repeated NFA.
        """
        min_repeats, max_repeats = self._parse_repeat_range()
        
        # Mandatory repetitions (min)
        repeated = a
        for _ in range(min_repeats - 1):
            second   = self._clone_nfa(repeated)
            repeated = self._concatenate(repeated, second)

        # Optional repetitions (for n <  max)
        if max_repeats is not None:
            for _ in range(max_repeats - min_repeats):
                second   = self._optional(self._clone_nfa(repeated))
                repeated = self._concatenate(repeated, second)
        else:
            # Infinite (like {n,})
            second   = self._kleene_star(self._clone_nfa(a))
            repeated = self._concatenate(repeated, second)
        
        return repeated
                    
    def _parse_repeat_range(self) -> Tuple[int, Optional[int]]:
        """Parses the contents inside { and } to determine the repeat range.

        ### Returns:
            Tuple: (min_repeats, max_repeats) where max_repeats can be None for unbounded
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
            
        # If there's a number after the comma
        num_string = ''
        while (peek := self._peek()) and peek.isdigit():
            num_string += self._consume()
        
        if num_string:
            max_value = int(num_string)
            
        self._consume('}')
        return (min_value, max_value)
    
    def _clone_nfa(self, nfa: NFA) -> NFA:
        return deepcopy(nfa)

    def _dot(self) -> NFA:
        """
        Constructs an NFA that matches any single character.

        ### Returns:
            NFA: The NFA for any character.
        """
        start = State()
        end   = State()
        dot   = TransitionLabel('.', is_wildcard=True)
        start.add_transition(dot, end)
        return NFA(start, end)
    
    def _character_class(self) -> NFA:
        """
        Constructs an NFA that matches character class.

        ### Returns:
            NFA: The NFA for characters.
        """
        start = State()
        end   = State()
        while (peek := self._peek()) and peek != ']':
            next_char = self._consume()
            symbol    = TransitionLabel(next_char, is_wildcard=False)
            start.add_transition(symbol, end)
        return NFA(start, end)

    def _peek(self) -> Optional[str]:
        """
        Returns the next character in the pattern without consuming it.

        ### Returns:
            Optional[str]: The next character, or None if at the end.
        """
        return self.pattern[self.pos] if self.pos < len(self.pattern) else None

    def _consume(self, expected: Optional[str] = None) -> str:
        """
        Consumes and returns the next character in the pattern.

        ### Args:
            expected (Optional[str]): If provided, raises an error if the next character does not match.

        ### Returns:
            str: The consumed character.

        ### Raises:
            ValueError: If the end of the pattern is reached or the expected character does not match.
        """
        if self.pos >= len(self.pattern):
            raise ValueError(f"Unexpected end of pattern. Expected {ascii(expected)}")
        char = self.pattern[self.pos]
        if expected and char != expected:
            raise ValueError(f"Expected {ascii(expected)} but got {ascii(char)} at index {self.pos}")
        self.pos += 1
        return char