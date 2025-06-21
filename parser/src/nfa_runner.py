from nfa import TransitionLabel, State, NFA
from typing import Set, List, Tuple


class MatchResult:
    """
    Represents the result of a match operation, containing the matched string and its span.

    Attributes:
        fullmatch (str): The entire matched string.
        start (int): The starting index of the match.
        end (int): The ending index of the match.
        groups (List[str]): List of captured groups in the match.
        group_spans (List[Tuple[int, int]]): List of spans for each captured group.
    """
    def __init__(self, fullmatch: str,
                 start: int, end: int, 
                 groups: List[str] = [], group_spans: List[Tuple[int, int]] = []) -> None:
        """
        Initialize a MatchResult instance.

        Args:
            fullmatch (str): The entire matched string.
            start (int): The starting index of the match.
            end (int): The ending index of the match.
            groups (List[str], optional): List of captured groups. Defaults to [].
            group_spans (List[Tuple[int, int]], optional): Spans for each group. Defaults to [].
        """
        self.__fullmatch = fullmatch
        self.__start     = start
        self.__end       = end
        self.__groups    = groups
        self.__spans     = group_spans

    def group(self, n=0) -> str:
        """
        Return the matched group.

        Args:
            n (int, optional): Group number. 0 for the whole match. Defaults to 0.

        Returns:
            str: The matched group string.
        """
        return self.__fullmatch if n == 0 else self.__groups[n - 1]
    
    @property
    def groups(self) -> Tuple[str, ...]:
        """
        Return all captured groups as a tuple.

        Returns:
            Tuple[str, ...]: All captured groups.
        """
        return tuple(self.__groups)
    
    def start(self, n=0) -> int:
        """
        Return the start index of the match or group.

        Args:
            n (int, optional): Group number. 0 for the whole match. Defaults to 0.

        Returns:
            int: The start index.
        """
        return self.__start if n == 0 else self.__spans[n - 1][0]
        
    def end(self, n=0) -> int:
        """
        Return the end index of the match or group.

        Args:
            n (int, optional): Group number. 0 for the whole match. Defaults to 0.

        Returns:
            int: The end index.
        """
        return self.__end if n == 0 else self.__spans[n - 1][1]
    
    def spans(self, n=0) -> Tuple[int, int]:
        """
        Return the (start, end) span of the match or group.

        Args:
            n (int, optional): Group number. 0 for the whole match. Defaults to 0.

        Returns:
            Tuple[int, int]: The (start, end) span.
        """
        return (self.start(n), self.end(n))

    def __repr__(self) -> str:
        """
        Return a string representation of the MatchResult.

        Returns:
            str: String representation.
        """
        return f"<Match(span={self.spans()}, match={self.__fullmatch!r})>"
    

class NFARunner:
    """
    Executes an NFA on a given input string, supporting anchors and dot (.) as any character.

    Attributes:
        nfa (NFA): The NFA to execute.
        anchor_start (bool): If True, match must start at the beginning.
        anchor_end (bool): If True, match must end at the end.
    """
    def __init__(self, nfa: NFA, anchor_start=False, anchor_end=False):
        """
        Initializes the runner with the NFA and anchor flags.

        Args:
            nfa (NFA): The NFA to execute.
            anchor_start (bool): If True, match must start at the beginning.
            anchor_end (bool): If True, match must end at the end.
        """
        self.nfa          = nfa
        self.anchor_start = anchor_start
        self.anchor_end   = anchor_end

    def _epsilon_closure(self, states: Set[State]) -> Set[State]:
        """
        Computes the epsilon closure of a set of states.

        Args:
            states (Set[State]): The initial set of states.

        Returns:
            Set[State]: The epsilon closure.
        """
        stack   = list(states)
        closure = set(states)
        while stack:
            state   = stack.pop()
            epsilon = TransitionLabel(None)
            for next_state in state.transitions.get(epsilon, []):
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
        return closure

    def run(self, s: str) -> bool:
        """
        Runs the NFA on the input string.

        Args:
            s (str): The input string.

        Returns:
            bool: True if the NFA matches the string, False otherwise.
        """
        # Determine starting positions based on anchor
        start_positions = [0] if self.anchor_start else range(len(s) + 1)

        for start_idx in start_positions:
            if self._match_from_position(s, start_idx):
                return True
        return False

    def _match_from_position(self, s: str, start_idx: int) -> bool:
        """
        Attempts to match the NFA from a specific position in the input string.

        Args:
            s (str): The input string.
            start_idx (int): The position to start matching from.

        Returns:
            bool: True if a match is found, False otherwise.
        """
        current_states = self._epsilon_closure({self.nfa.start})

        for char in s[start_idx:]:
            current_states = self._get_next_states(current_states, char)
            if not current_states:
                break

        if self.anchor_end:
            return self.nfa.accept in current_states and (start_idx + len(s[start_idx:]) == len(s))
        return self.nfa.accept in current_states

    def _get_next_states(self, states: Set[State], char: str) -> Set[State]:
        """
        Computes the set of next states for a given input character.

        Args:
            states (Set[State]): The current set of states.
            char (str): The current input character.

        Returns:
            Set[State]: The set of next states after consuming the character.
        """
        next_states = set()
        for state in states:
            # Handle wildcard (dot)
            dot_label = TransitionLabel('.', is_wildcard=True)
            for target in state.transitions.get(dot_label, []):
                next_states.update(self._epsilon_closure({target}))
            # Handle literal/escaped character
            literal_label = TransitionLabel(char)
            for target in state.transitions.get(literal_label, []):
                next_states.update(self._epsilon_closure({target}))
        return next_states