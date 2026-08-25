"""Master Resume Analysis Orchestrator
Coordinates parsing, NLP preprocessing, skill extraction, ATS auditing, and scoring.
"""

from typing import BinaryIO, Dict, Optional, Union
from .parser import ResumeParser
from .preprocessor import TextPreprocessor
from .skill_extractor import SkillExtractor
from .experience_analyzer import ExperienceAnalyzer
from .education_analyzer import EducationAnalyzer
from .ats_checker import ATSChecker
from .jd_matcher import JobDescriptionMatcher
from .scorer import ResumeScorer
from .feedback import FeedbackGenerator


class ResumeReviewer:
    """End-to-end AI Resume Reviewer engine."""

    def __init__(self):
        self.parser = ResumeParser()
        self.preprocessor = TextPreprocessor()
        self.skill_extractor = SkillExtractor()
        self.experience_analyzer = ExperienceAnalyzer()
        self.education_analyzer = EducationAnalyzer()
        self.ats_checker = ATSChecker()
        self.jd_matcher = JobDescriptionMatcher()
        self.scorer = ResumeScorer()
        self.feedback_generator = FeedbackGenerator()

    def analyze_resume(
        self,
        resume_source: Union[str, BinaryIO, bytes],
        job_description: Optional[str] = None,
        filename: str = ""
    ) -> Dict:
        """Runs the complete resume analysis pipeline.

        Args:
            resume_source: File path, raw string, byte array, or open file stream.
            job_description: Optional target job description to compute alignment.
            filename: Optional file name to aid format detection.

        Returns:
            Dict containing parsed data, extracted features, scores, and feedback.
        """
        # 1. Document Extraction
        raw_text = self.parser.parse(resume_source, filename=filename)
        cleaned_text = self.preprocessor.clean_text(raw_text)

        # 2. NLP Preprocessing & Statistics
        _, tokens = self.preprocessor.tokenize_and_lemmatize(cleaned_text)
        stats = self.preprocessor.get_text_statistics(cleaned_text)
        sections = self.preprocessor.segment_sections(cleaned_text)

        # 3. Domain Extractions
        skills_data = self.skill_extractor.extract_skills(cleaned_text)
        exp_data = self.experience_analyzer.analyze(
            cleaned_text,
            experience_section_text=sections.get("experience", "")
        )
        edu_data = self.education_analyzer.analyze(
            cleaned_text,
            education_section_text=sections.get("education", "")
        )

        # 4. ATS Audit
        ats_data = self.ats_checker.check_ats_compatibility(
            cleaned_text,
            sections,
            stats["word_count"]
        )

        # 5. Job Description Matcher (Optional)
        jd_match_data = None
        if job_description and job_description.strip():
            jd_match_data = self.jd_matcher.match(
                cleaned_text,
                job_description,
                resume_skills=skills_data["all_technical"]
            )

        # 6. Scoring Computation
        score_data = self.scorer.calculate_total_score(
            skills_data=skills_data,
            exp_data=exp_data,
            edu_data=edu_data,
            ats_data=ats_data,
            stats=stats,
            sections=sections
        )

        # 7. Feedback Generation
        feedback_data = self.feedback_generator.generate_feedback(
            skills_data=skills_data,
            exp_data=exp_data,
            edu_data=edu_data,
            ats_data=ats_data,
            stats=stats,
            score_data=score_data,
            jd_match_data=jd_match_data
        )

        # 8. Executive Summary
        summary = self.generate_summary(score_data, skills_data, exp_data, ats_data, jd_match_data)

        return {
            "metadata": {
                "task_id": "AI-SS-004",
                "student_code": "DAS005423",
                "version": "1.0.0"
            },
            "statistics": stats,
            "sections_detected": {k: len(v) > 0 for k, v in sections.items()},
            "skills": skills_data,
            "experience": exp_data,
            "education": edu_data,
            "ats_compatibility": ats_data,
            "job_match": jd_match_data,
            "scoring": score_data,
            "feedback": feedback_data,
            "summary": summary,
            "raw_text": cleaned_text
        }

    def generate_summary(
        self,
        score_data: Dict,
        skills_data: Dict,
        exp_data: Dict,
        ats_data: Dict,
        jd_match_data: Optional[Dict] = None
    ) -> str:
        """Formats an executive textual summary of the evaluation."""
        total = score_data["total_score"]
        grade = score_data["letter_grade"]
        lines = [
            f"📊 Overall Resume Score: {total}/100 ({grade})",
            f"🛠️ Technical Skills Found: {skills_data['technical_count']} ({', '.join(skills_data['all_technical'][:6])}...)",
            f"💬 Soft Skills Found: {skills_data['soft_count']}",
            f"💼 Experience: ~{exp_data['years']} Years ({exp_data['seniority_level']})",
            f"🤖 ATS Compatibility: {ats_data['ats_score']}/100 ({ats_data['status']})"
        ]
        if jd_match_data and jd_match_data.get("is_active"):
            lines.append(f"🎯 Job Match Alignment: {jd_match_data['match_score']}% ({jd_match_data['match_level']})")

        return "\n".join(lines)

