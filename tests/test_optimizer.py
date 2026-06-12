import unittest
from src.optimizer import optimize_prompt

class TestOptimizer(unittest.TestCase):

    def test_long_polite(self):
        prompt = ("Please kindly, if you don’t mind, could you actually provide me with a very detailed "
                  "explanation in order to help me understand the importance of incident management in IT systems "
                  "as soon as possible, because I really need it urgently.")
        expected = "Explain importance of incident management in IT systems quickly urgent"
        self.assertEqual(optimize_prompt(prompt), expected)

    def test_wordy_academic(self):
        prompt = ("In order to effectively comprehend the multifaceted role of artificial intelligence in modern "
                  "education systems, please kindly elaborate in a very detailed manner, covering a large number of "
                  "aspects including personalization, automation, and efficiency improvements due to the fact that these are critical.")
        expected = "Explain role of artificial intelligence in modern education systems covering personalization automation efficiency because critical"
        self.assertEqual(optimize_prompt(prompt), expected)

    def test_business_request(self):
        prompt = ("Please kindly just draft a very comprehensive summary that basically explains why escalation handling "
                  "and monitoring are really very important in IT support workflows, in order to ensure uptime and service continuity as soon as possible.")
        expected = "Draft summary explaining importance of escalation handling and monitoring in IT support workflows to ensure uptime quickly"
        self.assertEqual(optimize_prompt(prompt), expected)

    def test_extra_filler(self):
        prompt = ("Kind of, sort of, could you please explain in order to help me understand why documentation is very important "
                  "in IT workflows as soon as possible.")
        expected = "Explain why documentation is critical in IT workflows quickly"
        self.assertEqual(optimize_prompt(prompt), expected)

    def test_short_command(self):
        prompt = "Please summarize the quarterly report"
        expected = "Summarize the quarterly report"
        self.assertEqual(optimize_prompt(prompt), expected)

if __name__ == "__main__":
    unittest.main()
