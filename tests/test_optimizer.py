import unittest
from src.optimizer import optimize_prompt

class TestOptimizer(unittest.TestCase):
    def test_basic_prompt(self):
        self.assertEqual(optimize_prompt(" Hello "), "Optimized: Hello")

    def test_filler_removal(self):
        self.assertEqual(optimize_prompt("Please kindly write a summary"), "Optimized: write a summary")

if __name__ == "__main__":
    unittest.main()
def test_phrase_shortening(self):
    self.assertEqual(
        optimize_prompt("Please kindly write a very detailed summary in order to explain AI in education as soon as possible."),
        "write detailed summary to explain AI in education quickly"
    )
