"""ATS (Applicant Tracking System) Compatibility Checker
Audits resume structure, contact information, standard section headers, and formatting hygiene.
"""

import re
from typing import Dict, List


class ATSChecker:
    """Evaluates how well a resume complies with modern ATS parsing standards."""

    # Regex patterns for contact elements
    EMAIL_PATTERN = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    PHONE_PATTERN = r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|\b\d{10}\b"
    LINKEDIN_PATTERN = r"(?:linkedin\.com/in/[\w-]+|linkedin:\s*[\w-]+)"
    GITHUB_PATTERN = r"(?:github\.com/[\w-]+|github:\s*[\w-]+)"

    REQUIRED_SECTIONS = [
        "experience", "education", "skills"
    ]

    RECOMMENDED_SECTIONS = [
        "summary", "projects", "certifications"
    ]

    def extract_contact_info(self, text: str) -> Dict:
        """Extracts and validates candidate contact details."""
        emails = re.findall(self.EMAIL_PATTERN, text)
        phones = re.findall(self.PHONE_PATTERN, text)
        linkedin = re.findall(self.LINKEDIN_PATTERN, text, re.IGNORECASE)
        github = re.findall(self.GITHUB_PATTERN, text, re.IGNORECASE)

        return {
            "email": emails[0] if emails else None,
            "has_email": len(emails) > 0,
            "phone": phones[0] if phones else None,
            "has_phone": len(phones) > 0,
            "linkedin": linkedin[0] if linkedin else None,
            "has_linkedin": len(linkedin) > 0,
            "github": github[0] if github else None,
            "has_github": len(github) > 0
        }

    def audit_sections(self, detected_sections: Dict[str, str]) -> Dict:
        """Checks presence of standard ATS-friendly section headers."""
        present_sections = [
            sec for sec, content in detected_sections.items()
            if len(content.strip()) > 15 and sec not in ["header", "other"]
        ]

        missing_required = [sec for sec in self.REQUIRED_SECTIONS if sec not in present_sections]
        missing_recommended = [sec for sec in self.RECOMMENDED_SECTIONS if sec not in present_sections]

        return {
            "present_sections": present_sections,
            "missing_required": missing_required,
            "missing_recommended": missing_recommended,
            "sections_score": max(0, 100 - (len(missing_required) * 25 + len(missing_recommended) * 10))
        }

    def audit_formatting(self, text: str, word_count: int) -> Dict:
        """Audits length, bullet points, and formatting hygiene."""
        issues = []
        strengths = []

        # Length check
        if word_count < 200:
            issues.append("Resume is too brief (< 200 words). Add more details about your work and projects.")
        elif word_count > 1000:
            issues.append("Resume is lengthy (> 1,000 words). Aim for a concise 1-2 page structure (400-750 words).")
        else:
            strengths.append("Optimal resume length (400 - 800 words).")

        # Bullet points check
        bullet_count = len(re.findall(r"^[ \t]*[•\-\*\>]\s+", text, re.MULTILINE))
        if bullet_count < 4:
            issues.append("Few or no bullet points detected. Bullet points improve ATS readability and recruiter scanning.")
        else:
            strengths.append(f"Good use of bullet points ({bullet_count} bullets detected).")

        # Complex table / column / weird symbol check
        weird_chars = len(re.findall(r"[^\x00-\x7F\u2022\u2013\u2014]", text))
        if weird_chars > 20:
            issues.append("Detected non-standard symbols or emojis that may disrupt legacy ATS parsers.")
        else:
            strengths.append("Clean text formatting without disruptive special characters.")

        return {
            "bullet_count": bullet_count,
            "formatting_issues": issues,
            "formatting_strengths": strengths
        }

    def check_ats_compatibility(self, raw_text: str, detected_sections: Dict[str, str], word_count: int) -> Dict:
        """Calculates comprehensive ATS compatibility score and checks."""
        contact = self.extract_contact_info(raw_text)
        sections = self.audit_sections(detected_sections)
        formatting = self.audit_formatting(raw_text, word_count)

        # Calculate ATS score (out of 100)
        score = 0

        # Contact info (30 pts)
        if contact["has_email"]:
            score += 12
        if contact["has_phone"]:
            score += 10
        if contact["has_linkedin"] or contact["has_github"]:
            score += 8

        # Section headers (40 pts)
        score += int(sections["sections_score"] * 0.4)

        # Formatting & Length (30 pts)
        if 250 <= word_count <= 950:
            score += 15
        elif 150 <= word_count <= 1200:
            score += 8

        if formatting["bullet_count"] >= 4:
            score += 15
        elif formatting["bullet_count"] >= 1:
            score += 8

        score = min(max(score, 0), 100)

        # Status categorization
        if score >= 80:
            status = "ATS Ready (High Compatibility)"
        elif score >= 60:
            status = "Moderate (Needs Minor Fixes)"
        else:
            status = "Low Compatibility (Needs Overhaul)"

        return {
            "ats_score": score,
            "status": status,
            "contact_info": contact,
            "section_audit": sections,
            "formatting_audit": formatting
        }

