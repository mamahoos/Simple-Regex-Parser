import unittest
from parser import RegexParser, NFARunner, compile as compile_pattern

class TestRegexEngine(unittest.TestCase):
    def test_simple_literal(self):
        runner = compile_pattern("abc")
        self.assertTrue(runner.run("abc"))
        self.assertFalse(runner.run("ab"))
        self.assertFalse(runner.run("abcd"))

    def test_dot_operator(self):
        runner = compile_pattern("a.c")
        self.assertTrue(runner.run("abc"))
        self.assertTrue(runner.run("a9c"))
        self.assertFalse(runner.run("ac"))
        self.assertFalse(runner.run("abbc"))

    def test_star_operator(self):
        runner = compile_pattern("ab*")
        self.assertTrue(runner.run("a"))
        self.assertTrue(runner.run("ab"))
        self.assertTrue(runner.run("abbb"))
        self.assertFalse(runner.run("b"))
        self.assertFalse(runner.run("ba"))

    def test_plus_operator(self):
        runner = compile_pattern("ab+")
        self.assertFalse(runner.run("a"))
        self.assertTrue(runner.run("ab"))
        self.assertTrue(runner.run("abbbbb"))
        self.assertFalse(runner.run("b"))

    def test_question_operator(self):
        runner = compile_pattern("ab?")
        self.assertTrue(runner.run("a"))
        self.assertTrue(runner.run("ab"))
        self.assertFalse(runner.run("abb"))
        self.assertFalse(runner.run("b"))

    def test_alternation(self):
        runner = compile_pattern("a|b")
        self.assertTrue(runner.run("a"))
        self.assertTrue(runner.run("b"))
        self.assertFalse(runner.run("ab"))
        self.assertFalse(runner.run("c"))

    def test_grouping(self):
        runner = compile_pattern("(ab)*c")
        self.assertTrue(runner.run("c"))
        self.assertTrue(runner.run("abc"))
        self.assertTrue(runner.run("abababc"))
        self.assertFalse(runner.run("ab"))
        self.assertFalse(runner.run("ababcab"))

    def test_anchor_start(self):
        runner = compile_pattern("^abc")
        self.assertTrue(runner.run("abc"))
        self.assertFalse(runner.run("aabc"))
        self.assertFalse(runner.run("zabc"))

    def test_anchor_end(self):
        runner = compile_pattern("abc$")
        self.assertTrue(runner.run("abc"))
        self.assertFalse(runner.run("abcz"))
        self.assertFalse(runner.run("aabc"))

    def test_anchor_start_and_end(self):
        runner = compile_pattern("^abc$")
        self.assertTrue(runner.run("abc"))
        self.assertFalse(runner.run("abcc"))
        self.assertFalse(runner.run("aabc"))
        self.assertFalse(runner.run("abcabc"))
    
if __name__ == "__main__":
    unittest.main()