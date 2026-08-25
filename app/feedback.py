"""Intelligent Feedback Generation Engine
Produces targeted, actionable recommendations, strengths, and prioritized improvement steps.
"""

from typing import Dict, List


class FeedbackGenerator:
    """Generates structured, practical resume optimization feedback."""

    def generate_feedback(
        self,
        skills_data: Dict,
        exp_data: Dict,
        edu_data: Dict,
        ats_data: Dict,
        stats: Dict,
        score_data: Dict,
        jd_match_data: Dict = None
    ) -> Dict:
        """Constructs rich feedback across strengths, improvements, and next steps."""
        strengths: List[str] = []
        improvements: List[str] = []
        ats_tips: List[str] = []
        action_steps: List[str] = []

        total_score = score_data["total_score"]

        # --- 1. Skills Feedback ---
        tech_count = skills_data["technical_count"]
        soft_count = skills_data["soft_count"]

        if tech_count >= 8:
            strengths.append(f"Strong technical skill variety ({tech_count} technical skills identified across domains).")
        elif tech_count < 4:
            improvements.append("Expand your technical skills list with specific programming languages, frameworks, or cloud tools.")
            action_steps.append("Add 3-5 core technical competencies relevant to your target role.")

        if soft_count >= 3:
            strengths.append(f"Good balance of soft skills ({soft_count} interpersonal/leadership attributes detected).")
        else:
            improvements.append("Include essential soft skills such as 'Cross-Functional Collaboration', 'Problem Solving', or 'Agile Delivery'.")

        # --- 2. Experience & Metrics Feedback ---
        years = exp_data["years"]
        verbs = exp_data["action_verbs"]
        metrics_count = exp_data["metrics_count"]

        if exp_data["has_experience"]:
            if years > 0:
                strengths.append(f"Clear career progression with ~{years} years of relevant experience detected.")
            if metrics_count >= 3:
                strengths.append(f"Excellent quantifiable impact! Found {metrics_count} measurable achievements (percentages, revenue, or scale).")
            elif metrics_count == 0:
                improvements.append("Transform bullet points from task descriptions to quantified business results (e.g., 'increased throughput by 35%', 'reduced costs by $10K').")
                action_steps.append("Quantify at least 2 key project accomplishments with numbers or percentages.")
        else:
            improvements.append("No explicit work history detected. If you are a fresher/student, prominently showcase academic projects, open-source contributions, or internships.")
            action_steps.append("Add a detailed 'Projects & Internships' section demonstrating practical problem solving.")

        if verbs["strong_verbs_count"] >= 4:
            strengths.append(f"High-impact phrasing with {verbs['strong_verbs_count']} dynamic action verbs.")
        elif verbs["weak_phrases_count"] > 0:
            improvements.append(f"Replace passive phrases ({', '.join(verbs['weak_phrases'][:3])}) with punchy action verbs like 'Engineered', 'Optimized', or 'Spearheaded'.")

        # --- 3. Education Feedback ---
        if edu_data["has_education"]:
            highest = edu_data["highest_degree_level"].replace("_", " ").title()
            strengths.append(f"Educational qualification verified ({highest}).")
        else:
            improvements.append("Explicitly state your degree, major, university, and expected or completed graduation year.")
            action_steps.append("Structure your Education section with Degree, University Name, and Graduation Date.")

        # --- 4. ATS & Structure Feedback ---
        contact = ats_data["contact_info"]
        missing_sec = ats_data["section_audit"]["missing_required"]

        if not contact["has_email"] or not contact["has_phone"]:
            ats_tips.append("Missing essential contact details (ensure email and direct phone number are in the header).")
            action_steps.append("Add contact header with email, phone number, and LinkedIn URL.")
        else:
            strengths.append("Standard contact information (email & phone) clearly present.")

        if contact["has_linkedin"] or contact["has_github"]:
            strengths.append("Professional profile links (LinkedIn/GitHub) present.")
        else:
            ats_tips.append("Add your LinkedIn profile link and GitHub/Portfolio URL to boost credibility.")

        if missing_sec:
            ats_tips.append(f"ATS parsers look for standard headings. Missing: {', '.join([s.title() for s in missing_sec])}.")

        word_count = stats["word_count"]
        if word_count < 250:
            ats_tips.append(f"Your resume word count ({word_count} words) is below standard. Aim for 400–700 words.")
        elif word_count > 900:
            ats_tips.append(f"Your resume word count ({word_count} words) is long. Consider condensing to 1-2 pages.")

        # --- 5. Job Match Feedback (if active) ---
        if jd_match_data and jd_match_data.get("is_active"):
            match_score = jd_match_data["match_score"]
            missing_kw = jd_match_data["missing_keywords"]
            if match_score >= 70:
                strengths.append(f"Outstanding job match alignment ({match_score}%) with target position!")
            else:
                improvements.append(f"Job alignment score is {match_score}%. Incorporate missing keywords: {', '.join(missing_kw[:5])}.")
                action_steps.append(f"Integrate target keywords ({', '.join(missing_kw[:3])}) into project bullet points.")

        # Top 3 prioritized steps
        if not action_steps:
            if total_score >= 85:
                action_steps = ["Polish formatting and tailor project descriptions for specific company job descriptions."]
            else:
                action_steps = ["Review bullet point action verbs and ensure all tools/frameworks are listed under Skills."]

        return {
            "strengths": strengths,
            "areas_for_improvement": improvements,
            "ats_recommendations": ats_tips,
            "prioritized_next_steps": action_steps[:3]
        }

