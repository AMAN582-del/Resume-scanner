import unittest

from resume_scanner import extract_keywords, rank_resumes, score_resume


class ResumeScannerTests(unittest.TestCase):
    def test_extract_keywords_filters_common_words(self):
        job_description = (
            "We are hiring a Python developer with SQL and API integration skills. "
            "Python knowledge and SQL optimization are required."
        )

        keywords = extract_keywords(job_description)

        self.assertIn("python", keywords)
        self.assertIn("sql", keywords)
        self.assertNotIn("with", keywords)

    def test_score_resume_returns_percentage(self):
        job_description = "python sql docker"
        resume_text = "Experienced in Python and SQL."

        result = score_resume(job_description, resume_text)

        self.assertAlmostEqual(result["score"], 66.67, places=2)
        self.assertIn("python", result["matched_keywords"])
        self.assertIn("sql", result["matched_keywords"])
        self.assertNotIn("sql", result["missing_keywords"])
        self.assertIn("docker", result["missing_keywords"])

    def test_rank_resumes_orders_best_match_first(self):
        job_description = "python sql docker"
        resumes = {
            "alice.txt": "python sql docker kubernetes",
            "bob.txt": "python sql",
        }

        ranked = rank_resumes(job_description, resumes)

        self.assertEqual(ranked[0]["candidate"], "alice.txt")
        self.assertGreater(ranked[0]["score"], ranked[1]["score"])


if __name__ == "__main__":
    unittest.main()
