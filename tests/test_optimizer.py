import unittest
from src.optimizer import optimize_prompt, optimize_suggestions

class TestOptimizer(unittest.TestCase):

    def test_hello_world_variants(self):
        p = "I said that have to optimise but that not happened why I want the answer, write a code related to python which gives the helloworld program"
        self.assertEqual(optimize_prompt(p), "Write Python code to print Hello World")

    def test_long_polite(self):
        p = ("Please kindly, if you don’t mind, could you actually provide me with a very detailed explanation "
             "in order to help me understand the importance of incident management in IT systems as soon as possible, "
             "because I really need it urgently.")
        self.assertEqual(optimize_prompt(p), "Explain importance of incident management in IT systems quickly")

    def test_academic(self):
        p = ("In order to effectively comprehend the multifaceted role of artificial intelligence in modern education systems, "
             "please kindly elaborate in a very detailed manner, covering a large number of aspects including personalization, automation, and efficiency improvements due to the fact that these are critical.")
        out = optimize_prompt(p)
        self.assertTrue("Explain" in out and "artificial intelligence" in out)

    def test_business(self):
        p = ("Please kindly just draft a very comprehensive summary that basically explains why escalation handling and monitoring "
             "are really very important in IT support workflows, in order to ensure uptime and service continuity as soon as possible.")
        out = optimize_prompt(p)
        self.assertTrue("Draft" in out or "Summarize" in out)

    def test_suggestions_api(self):
        p = "Please summarize the quarterly report"
        opts = optimize_suggestions(p)
        self.assertEqual(len(opts), 3)
        self.assertTrue(any(o["style"] == "balanced" for o in opts))

if __name__ == "__main__":
    unittest.main()
