import unittest
from main import compile_pattern, match_pattern

class TestRegexEngine(unittest.TestCase):
    def test_literal_match(self):
        self.assertTrue(match_pattern("abc", "abc"))
        self.assertFalse(match_pattern("abc", "ab"))
        self.assertFalse(match_pattern("abc", "abcd"))

    def test_dot_operator(self):
        self.assertTrue(match_pattern("a.c", "abc"))
        self.assertTrue(match_pattern("a.c", "a9c"))
        self.assertFalse(match_pattern("a.c", "ac"))

    def test_star_operator(self):
        self.assertTrue(match_pattern("ab*c", "ac"))
        self.assertTrue(match_pattern("ab*c", "abc"))
        self.assertTrue(match_pattern("ab*c", "abbbc"))
        self.assertFalse(match_pattern("ab*c", "abbdc"))

    def test_plus_operator(self):
        self.assertTrue(match_pattern("ab+c", "abc"))
        self.assertTrue(match_pattern("ab+c", "abbbbbc"))
        self.assertFalse(match_pattern("ab+c", "ac"))

    def test_question_operator(self):
        self.assertTrue(match_pattern("ab?c", "ac"))
        self.assertTrue(match_pattern("ab?c", "abc"))
        self.assertFalse(match_pattern("ab?c", "abbc"))

    def test_anchor_start(self):
        self.assertTrue(match_pattern("^abc", "abc"))
        self.assertFalse(match_pattern("^abc", "xabc"))

    def test_anchor_end(self):
        self.assertTrue(match_pattern("abc$", "abc"))
        self.assertFalse(match_pattern("abc$", "abcc"))

    def test_alternation(self):
        self.assertTrue(match_pattern("a|b", "a"))
        self.assertTrue(match_pattern("a|b", "b"))
        self.assertFalse(match_pattern("a|b", "c"))

    def test_compile_pattern_runner(self):
        runner = compile_pattern("a.c")
        self.assertTrue(runner.run("abc"))
        self.assertFalse(runner.run("ac"))
        
    def test_empty_pattern(self):
        self.assertTrue(match_pattern("", ""))
        self.assertFalse(match_pattern("", "a"))
    def test_empty_string(self):
        self.assertFalse(match_pattern("a", ""))
        self.assertTrue(match_pattern("a*", ""))
    def test_multiple_operators(self):
        self.assertTrue(match_pattern("a.*c", "axyzc"))
        self.assertFalse(match_pattern("a.*c", "axyz"))
        self.assertTrue(match_pattern("ab+c?", "abbb"))
        self.assertTrue(match_pattern("ab+c?", "abbbc"))
        self.assertFalse(match_pattern("ab+c?", "ac"))
    def test_nested_alternation(self):
        self.assertTrue(match_pattern("a|(b|c)", "a"))
        self.assertTrue(match_pattern("a|(b|c)", "b"))
        self.assertTrue(match_pattern("a|(b|c)", "c"))
        self.assertFalse(match_pattern("a|(b|c)", "d"))
    def test_combined_anchors(self):
        self.assertTrue(match_pattern("^abc$", "abc"))
        self.assertFalse(match_pattern("^abc$", "abcc"))
        self.assertFalse(match_pattern("^abc$", "xabc"))
    def test_escape_characters(self):
        self.assertTrue(match_pattern(r"a\.c", "a.c"))
        self.assertFalse(match_pattern(r"a\.c", "abc"))
    def test_longer_strings(self):
        self.assertTrue(match_pattern("abc", "abcabc",))
        self.assertFalse(match_pattern("^abc$", "abcabc"))
        self.assertFalse(match_pattern("^abc$", "aabc"))
    def test_multiple_question(self):
        self.assertTrue(match_pattern("ab??c", "ac"))
        self.assertTrue(match_pattern("ab??c", "abc"))
        self.assertFalse(match_pattern("ab??c", "abbc"))
    def test_complex_nested(self):
        self.assertTrue(match_pattern("^(a|b)*c+d?$", "abababcc"))
        self.assertTrue(match_pattern("^(a|b)*c+d?$", "abcc"))
        self.assertTrue(match_pattern("^(a|b)*c+d?$", "cc"))
        self.assertTrue(match_pattern("^(a|b)*c+d?$", "ccdd"[:-1]))  # "ccd"
        self.assertFalse(match_pattern("^(a|b)*c+d?$", "abac"))
        self.assertFalse(match_pattern("^(a|b)*c+d?$", "abccx"))
    def test_multiple_alternations(self):
        self.assertTrue(match_pattern("a|b|c|d", "a"))
        self.assertTrue(match_pattern("a|b|c|d", "d"))
        self.assertFalse(match_pattern("a|b|c|d", "e"))
    def test_star_plus_question(self):
        self.assertTrue(match_pattern("ab*cd+e?", "acd"))
        self.assertTrue(match_pattern("ab*cd+e?", "abbbcdde"))
        self.assertTrue(match_pattern("ab*cd+e?", "abccd"))
        self.assertFalse(match_pattern("ab*cd+e?", "abcc"))
        self.assertFalse(match_pattern("ab*cd+e?", "abbbccddeee"))
    def test_dot_and_anchors(self):
        self.assertTrue(match_pattern("^a.c$", "abc"))
        self.assertTrue(match_pattern("^a.c$", "a9c"))
        self.assertFalse(match_pattern("^a.c$", "a9cd"))
        self.assertFalse(match_pattern("^a.c$", "ba9c"))
    def test_escape_and_operators(self):
        self.assertTrue(match_pattern(r"ab\*c", "ab*c"))
        self.assertFalse(match_pattern(r"ab\*c", "abbc"))
        self.assertTrue(match_pattern(r"\^abc\$", "^abc$"))
        self.assertFalse(match_pattern(r"\^abc\$", "abc"))
if __name__ == "__main__":
    unittest.main()