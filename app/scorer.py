"""Composite Resume Scoring Engine
Calculates weighted scores across Skills, Experience, Education, ATS Compatibility, and Depth.
"""

from typing import Dict


class ResumeScorer:
    """Computes transparent, granular scores out of 100 with category breakdowns."""

    def score_skills(self, skills_data: Dict) -> Dict:
        """Score skills out of 30 points."""
        tech_count = skills_data["technical_count"]
        soft_count = skills_data["soft_count"]
        diversity = skills_data["diversity_ratio"]

        # Technical points (max 20)
        tech_score = min(tech_count * 2.5, 20.0)

        # Soft points (max 5)
        soft_score = min(soft_count * 1.5, 5.0)

        # Diversity points (max 5)
        diversity_score = diversity * 5.0

        total = round(min(tech_score + soft_score + diversity_score, 30.0), 1)

        return {
            "score": total,
            "max": 30,
            "breakdown": {
                "technical_skills": round(tech_score, 1),
                "soft_skills": round(soft_score, 1),
                "diversity_bonus": round(diversity_score, 1)
            }
        }

    def score_experience(self, exp_data: Dict) -> Dict:
        """Score experience and impact out of 25 points."""
        years = exp_data["years"]
        verbs = exp_data["action_verbs"]
        metrics_count = exp_data["metrics_count"]

        # Years points (max 12)
        if years >= 5:
            years_score = 12.0
        elif years >= 3:
            years_score = 10.0
        elif years >= 1:
            years_score = 7.0
        elif exp_data["has_experience"]:
            years_score = 4.0
        else:
            years_score = 0.0

        # Action verbs points (max 7)
        strong_verbs_count = verbs["strong_verbs_count"]
        verbs_score = min(strong_verbs_count * 1.5, 7.0)

        # Quantified metrics points (max 6)
        metrics_score = min(metrics_count * 2.0, 6.0)

        total = round(min(years_score + verbs_score + metrics_score, 25.0), 1)

        return {
            "score": total,
            "max": 25,
            "breakdown": {
                "experience_tenure": round(years_score, 1),
                "action_verbs": round(verbs_score, 1),
                "quantified_impact": round(metrics_score, 1)
            }
        }

    def score_education(self, edu_data: Dict) -> Dict:
        """Score education qualifications out of 15 points."""
        rank = edu_data["degree_rank"]
        majors_count = len(edu_data["majors_found"])
        institutions_count = len(edu_data["institutions_found"])

        # Base score by degree level (max 11)
        degree_map = {5: 11.0, 4: 10.0, 3: 8.5, 2: 6.0, 1: 3.0, 0: 0.0}
        base_degree_score = degree_map.get(rank, 0.0)

        # Major relevance bonus (max 2)
        major_bonus = min(majors_count * 1.5, 2.0)

        # Institution presence bonus (max 2)
        inst_bonus = min(institutions_count * 1.0, 2.0)

        total = round(min(base_degree_score + major_bonus + inst_bonus, 15.0), 1)

        return {
            "score": total,
            "max": 15,
            "breakdown": {
                "degree_level": round(base_degree_score, 1),
                "major_relevance": round(major_bonus, 1),
                "institution_presence": round(inst_bonus, 1)
            }
        }

    def score_ats_structure(self, ats_data: Dict) -> Dict:
        """Score ATS compatibility and structure out of 15 points."""
        raw_ats_score = ats_data["ats_score"]  # 0 to 100
        normalized = round((raw_ats_score / 100.0) * 15.0, 1)

        return {
            "score": normalized,
            "max": 15,
            "breakdown": {
                "ats_compliance": normalized
            }
        }

    def score_content_quality(self, stats: Dict, sections: Dict) -> Dict:
        """Score content depth and completeness out of 15 points."""
        word_count = stats["word_count"]

        # Word count points (max 8)
        if 400 <= word_count <= 850:
            length_score = 8.0
        elif 250 <= word_count <= 1100:
            length_score = 5.5
        elif word_count > 150:
            length_score = 3.0
        else:
            length_score = 1.0

        # Section presence depth (max 7)
        depth_sections = ["projects", "certifications", "summary", "awards"]
        present_depth_count = sum(1 for sec in depth_sections if len(sections.get(sec, "").strip()) > 15)
        section_depth_score = min(present_depth_count * 2.5, 7.0)

        total = round(min(length_score + section_depth_score, 15.0), 1)

        return {
            "score": total,
            "max": 15,
            "breakdown": {
                "length_appropriateness": round(length_score, 1),
                "section_richness": round(section_depth_score, 1)
            }
        }

    def get_letter_grade(self, total_score: float) -> str:
        """Assigns a letter grade based on overall score."""
        if total_score >= 90:
            return "A+ (Outstanding)"
        elif total_score >= 80:
            return "A (Excellent)"
        elif total_score >= 70:
            return "B+ (Very Good)"
        elif total_score >= 60:
            return "B (Good / Decent)"
        elif total_score >= 50:
            return "C (Needs Improvement)"
        elif total_score >= 40:
            return "D (Weak)"
        return "F (Needs Complete Overhaul)"

    def calculate_total_score(
        self,
        skills_data: Dict,
        exp_data: Dict,
        edu_data: Dict,
        ats_data: Dict,
        stats: Dict,
        sections: Dict
    ) -> Dict:
        """Aggregates all criteria into a unified score out of 100."""
        skills_res = self.score_skills(skills_data)
        exp_res = self.score_experience(exp_data)
        edu_res = self.score_education(edu_data)
        ats_res = self.score_ats_structure(ats_data)
        quality_res = self.score_content_quality(stats, sections)

        total = round(
            skills_res["score"] +
            exp_res["score"] +
            edu_res["score"] +
            ats_res["score"] +
            quality_res["score"],
            1
        )
        total = min(max(total, 0.0), 100.0)

        return {
            "total_score": total,
            "letter_grade": self.get_letter_grade(total),
            "categories": {
                "skills": skills_res,
                "experience": exp_res,
                "education": edu_res,
                "ats_formatting": ats_res,
                "content_quality": quality_res
            }
        }

