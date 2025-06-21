from regex_parser import RegexParser
from nfa_runner import NFARunner
from typing import Union

def compile_pattern(pattern: str) -> NFARunner:
    parser = RegexParser(pattern)
    nfa    = parser.parse()
    runner = NFARunner(nfa, parser.anchor_start, parser.anchor_end)
    return runner

def match_pattern(pattern: Union[str, NFARunner], string: str) -> bool:
    if not isinstance(pattern, NFARunner):
        pattern = compile_pattern(pattern)
    return pattern.run(string)