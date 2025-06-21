from typing import Optional, Dict, List


class TransitionLabel:
    """
    Represents a transition label on an NFA edge.

    Attributes:
        value (Optional[str]): The character that triggers this transition.
            None means epsilon (ε-transition).
            A single character represents a literal transition.
        is_wildcard (bool): If True, represents a dot (.) wildcard match.
    """
    __slots__ = ['value', 'is_wildcard']

    def __init__(self, value: Optional[str], is_wildcard: bool = False) -> None:
        """
        Initialize a TransitionLabel with a character or as a wildcard.

        Args:
            value (Optional[str]): The character for the transition, or None for epsilon.
            is_wildcard (bool, optional): If True, represents a wildcard (dot). Defaults to False.
        """
        self.value       = value
        self.is_wildcard = is_wildcard

    def is_epsilon(self) -> bool:
        """
        Check if this transition is an epsilon (ε) transition.

        Returns:
            bool: True if this is an epsilon transition, False otherwise.
        """
        return self.value is None and not self.is_wildcard    

    def __repr__(self) -> str:
        """
        Return a string representation of the TransitionLabel.

        Returns:
            str: String representation.
        """
        if self.is_wildcard:
            return "TransitionLabel(.)"
        if self.value is None:
            return "TransitionLabel(ε)"
        return f"TransitionLabel({repr(self.value)})"

    def __hash__(self) -> int:
        """
        Return the hash value of the TransitionLabel.

        Returns:
            int: Hash value.
        """
        attributes = (self.value, self.is_wildcard)
        return hash(attributes)

    def __eq__(self, other: 'TransitionLabel') -> bool:       # type: ignore
        """
        Check equality with another TransitionLabel.

        Args:
            other (TransitionLabel): The other TransitionLabel to compare.

        Returns:
            bool: True if equal, False otherwise.
        """
        if not isinstance(other, TransitionLabel):
            return False
        return self.value == other.value and \
                    self.is_wildcard == other.is_wildcard


class State:
    """
    Represents a state in the NFA with a set of transitions to other states.

    Attributes:
        transitions (Dict[TransitionLabel, List[State]]): Outgoing transitions from this state.
    """
    __slots__ = ['transitions']

    def __init__(self):
        """
        Initialize a new state with an empty dictionary of transitions.
        """
        self.transitions: Dict[TransitionLabel, List['State']] = {}

    def add_transition(self, symbol: TransitionLabel, state: 'State'):
        """
        Add a transition from this state to another state on the given symbol.

        Args:
            symbol (TransitionLabel): The symbol for the transition (None for epsilon).
            state (State): The state to transition to.
        """
        self.transitions.setdefault(symbol, []).append(state)

    def __repr__(self):
        """
        Return a string representation of the state and its transitions.

        Returns:
            str: String representation.
        """
        return f"State(transitions={self.transitions})"


class NFA:
    """
    Represents a Non-deterministic Finite Automaton (NFA) with a start and accept state.

    Attributes:
        start (State): The start state of the NFA.
        accept (State): The accept (final) state of the NFA.
    """
    __slots__ = ['start', 'accept']

    def __init__(self, start: State, accept: State):
        """
        Initialize the NFA with a start and accept state.

        Args:
            start (State): The start state of the NFA.
            accept (State): The accept (final) state of the NFA.
        """
        self.start  = start
        self.accept = accept

    def __repr__(self):
        """
        Return a string representation of the NFA.

        Returns:
            str: String representation.
        """
        return f"NFA(start={self.start}, accept={self.accept})"

