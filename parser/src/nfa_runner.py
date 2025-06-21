from nfa import TransitionLabel, State, NFA
from typing import Set


class NFARunner:
    """
    Executes an NFA on a given input string, supporting anchors and dot (.) as any character.
    """
    def __init__(self, nfa: NFA, anchor_start=False, anchor_end=False):
        """
        Initializes the runner with the NFA and anchor flags.

        ### Args:
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

        ### Args:
            states (Set[State]): The initial set of states.

        ### Returns:
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

        ### Args:
            s (str): The input string.

        ### Returns:
            bool: True if the NFA matches the string, False otherwise.
        """
        if self.anchor_start:
            positions = [0]
        else:
            positions = range(len(s) + 1)
            
        for pos in positions:
            current_states = self._epsilon_closure({self.nfa.start})
            for char in s[pos:]:
                next_states = set()
                for state in current_states:
                    # Dot: any character
                    dot = TransitionLabel('.', is_wildcard=True)
                    for target in state.transitions.get(dot, []):
                        next_states.update(self._epsilon_closure({target}))
                    # Literal/escaped
                    literal = TransitionLabel(char)
                    for target in state.transitions.get(literal, []):
                        next_states.update(self._epsilon_closure({target}))
                current_states = next_states
                
            if self.anchor_end:
                if self.nfa.accept in current_states and pos + len(s[pos:]) == len(s):
                    return True
            else:
                if self.nfa.accept in current_states:
                    return True
        return False