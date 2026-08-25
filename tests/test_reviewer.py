"""Test suite for AI Resume Reviewer components.
Verifies parser, preprocessor, skill extractor, experience, education, ATS checker, scorer, and matcher.
"""

import os
import unittest
from app.parser import ResumeParser
from app.preprocessor import TextPreprocessor
from app.skill_extractor import SkillExtractor
from app.experience_analyzer import ExperienceAnalyzer
from app.education_analyzer import EducationAnalyzer
from app.ats_checker import ATSChecker
from app.jd_matcher import JobDescriptionMatcher
from app.scorer import ResumeScorer
from app.feedback import FeedbackGenerator
from app.analyzer import ResumeReviewer


class TestResumeReviewer(unittest.TestCase):
    """Unit tests for all resume reviewer components."""

    def setUp(self):
        self.reviewer = ResumeReviewer()
        self.preprocessor = TextPreprocessor()
        self.skill_extractor = SkillExtractor()
        self.experience_analyzer = ExperienceAnalyzer()
        self.education_analyzer = EducationAnalyzer()
        self.ats_checker = ATSChecker()
        self.jd_matcher = JobDescriptionMatcher()
        self.scorer = ResumeScorer()

        self.sample_text = """
        Jane Doe
        jane.doe@example.com | (555) 123-4567 | linkedin.com/in/janedoe
        
        SUMMARY
        Senior Software Engineer with 5+ years of experience in Python, Cloud, and Machine Learning.
        
        SKILLS
        Python, Java, Docker, Kubernetes, AWS, PostgreSQL, Machine Learning, Leadership, Problem Solving.
        
        EXPERIENCE
        Senior Engineer | TechCorp (2020 - Present)
        • Architected distributed backend using Python and AWS, increasing throughput by 45%.
        • Spearheaded team of 5 developers and delivered 3 microservices on time.
        
        EDUCATION
        B.Tech in Computer Science | Global Tech Institute (2016 - 2020)
        """

    def test_preprocessor_stats(self):
        stats = self.preprocessor.get_text_statistics(self.sample_text)
        self.assertGreater(stats["word_count"], 40)
        self.assertGreater(stats["line_count"], 5)

    def test_section_segmentation(self):
        sections = self.preprocessor.segment_sections(self.sample_text)
        self.assertIn("skills", sections)
        self.assertIn("experience", sections)
        self.assertIn("education", sections)
        self.assertTrue(len(sections["skills"]) > 0)

    def test_skill_extraction(self):
        skills = self.skill_extractor.extract_skills(self.sample_text)
        self.assertIn("Python", skills["all_technical"])
        self.assertIn("AWS", skills["all_technical"])
        self.assertIn("Leadership", skills["soft_skills"])
        self.assertGreaterEqual(skills["technical_count"], 4)

    def test_experience_extraction(self):
        exp = self.experience_analyzer.analyze(self.sample_text)
        self.assertGreaterEqual(exp["years"], 4.0)
        self.assertTrue(exp["has_experience"])
        self.assertIn("architected", exp["action_verbs"]["strong_verbs"])
        self.assertGreater(len(exp["quantified_metrics"]), 0)

    def test_education_extraction(self):
        edu = self.education_analyzer.analyze(self.sample_text)
        self.assertTrue(edu["has_education"])
        self.assertEqual(edu["highest_degree_level"], "bachelors")
        self.assertIn("Computer Science", edu["majors_found"])

    def test_ats_checker(self):
        sections = self.preprocessor.segment_sections(self.sample_text)
        stats = self.preprocessor.get_text_statistics(self.sample_text)
        ats = self.ats_checker.check_ats_compatibility(self.sample_text, sections, stats["word_count"])
        self.assertTrue(ats["contact_info"]["has_email"])
        self.assertTrue(ats["contact_info"]["has_phone"])
        self.assertGreaterEqual(ats["ats_score"], 60)

    def test_jd_matcher(self):
        jd = "Looking for a Senior Python Software Engineer with AWS, Docker, Kubernetes and Machine Learning experience."
        match = self.jd_matcher.match(self.sample_text, jd)
        self.assertTrue(match["is_active"])
        self.assertGreaterEqual(match["match_score"], 30.0)
        self.assertIn("python", [t.lower() for t in match["matched_keywords"]])

    def test_full_pipeline_scores(self):
        result = self.reviewer.analyze_resume(self.sample_text)
        self.assertIn("scoring", result)
        score = result["scoring"]["total_score"]
        self.assertGreaterEqual(score, 60.0)
        self.assertLessEqual(score, 100.0)
        self.assertIn("feedback", result)
        self.assertTrue(len(result["feedback"]["strengths"]) > 0)

    def test_weak_resume_scoring(self):
        weak_text = "John. looking for computer job. did tasks and helped with bugs."
        result = self.reviewer.analyze_resume(weak_text)
        score = result["scoring"]["total_score"]
        self.assertLess(score, 50.0)
        self.assertTrue(len(result["feedback"]["areas_for_improvement"]) > 0)


if __name__ == "__main__":
    unittest.main()
