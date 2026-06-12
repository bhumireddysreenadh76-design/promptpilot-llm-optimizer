import unittest
from src.bot import optimize_prompt

class TestOptimizer(unittest.TestCase):
    def test_basic_prompt(self):
        self.assertEqual(optimize_prompt(" Hello "), "Optimized: Hello")

if __name__ == "__main__":
    unittest.main()
