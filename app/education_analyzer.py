"""Education & Academic Extraction Module
Extracts degrees, majors, universities, GPA/CGPA, and graduation years.
"""

import re
from typing import Dict, List, Optional


class EducationAnalyzer:
    """Parses and evaluates educational qualifications and academic achievements."""

    DEGREE_HIERARCHY = {
        "doctorate": {
            "weight": 5,
            "patterns": [
                r"\bph\.?d\b", r"\bdoctorate\b", r"\bdoctor of philosophy\b", r"\bd\.?phil\b"
            ]
        },
        "masters": {
            "weight": 4,
            "patterns": [
                r"\bm\.?tech\b", r"\bm\.?s\.?\b", r"\bm\.?sc\b", r"\bmba\b",
                r"\bmaster\s+of\s+(?:science|technology|engineering|business|arts|computer\s+applications)\b",
                r"\bmca\b", r"\bm\.?e\.?\b"
            ]
        },
        "bachelors": {
            "weight": 3,
            "patterns": [
                r"\bb\.?tech\b", r"\bb\.?e\.?\b", r"\bb\.?s\.?\b", r"\bb\.?sc\b",
                r"\bbachelor\s+of\s+(?:technology|engineering|science|arts|computer\s+applications|business\s+administration)\b",
                r"\bbca\b", r"\bbba\b", r"\bb\.?com\b"
            ]
        },
        "associate_diploma": {
            "weight": 2,
            "patterns": [
                r"\bassociate\s+degree\b", r"\bdiploma\b", r"\bassociate\s+of\s+science\b"
            ]
        },
        "high_school": {
            "weight": 1,
            "patterns": [
                r"\bhigh\s+school\b", r"\bsecondary\s+school\b", r"\b12th\b", r"\bcbse\b", r"\bicse\b"
            ]
        }
    }

    MAJORS = [
        "computer science", "data science", "information technology",
        "artificial intelligence", "machine learning", "software engineering",
        "electrical engineering", "electronics and communication", "mechanical engineering",
        "civil engineering", "mathematics", "statistics", "physics", "economics",
        "business administration", "finance", "information systems", "cybersecurity"
    ]

    INSTITUTION_KEYWORDS = [
        "university", "institute", "college", "school of", "academy",
        "polytechnic", "iit", "nit", "iiit", "bits"
    ]

    GPA_PATTERN = r"(?:gpa|cgpa|grade|marks|percentage|aggregate)\s*[:=-]?\s*(\d+(?:\.\d+)?)\s*(?:/\s*(\d+(?:\.\d+)?)|%)?"

    def extract_degrees(self, text: str) -> List[Dict]:
        """Detects all degrees mentioned and categorizes their highest level."""
        found_degrees = []
        text_lower = text.lower()

        for level, info in self.DEGREE_HIERARCHY.items():
            for pattern in info["patterns"]:
                match = re.search(pattern, text_lower)
                if match:
                    found_degrees.append({
                        "level": level,
                        "matched_text": match.group(0),
                        "rank": info["weight"]
                    })
                    break  # One match per level category is sufficient

        # Sort highest degree first
        return sorted(found_degrees, key=lambda x: x["rank"], reverse=True)

    def extract_majors(self, text: str) -> List[str]:
        """Identifies field of study or major."""
        text_lower = text.lower()
        found_majors = []
        for major in self.MAJORS:
            if re.search(rf"\b{re.escape(major)}\b", text_lower):
                found_majors.append(major.title())
        return found_majors

    def extract_institutions(self, text: str) -> List[str]:
        """Extracts college or university names."""
        lines = text.split("\n")
        institutions = []
        for line in lines:
            line_clean = line.strip()
            line_lower = line_clean.lower()
            if any(k in line_lower for k in self.INSTITUTION_KEYWORDS):
                # Filter out overly long lines
                if len(line_clean.split()) <= 10:
                    institutions.append(line_clean)
        return institutions[:3]

    def extract_gpa(self, text: str) -> Optional[str]:
        """Extracts GPA or percentage if listed."""
        match = re.search(self.GPA_PATTERN, text, re.IGNORECASE)
        if match:
            return match.group(0).strip()
        return None

    def analyze(self, raw_text: str, education_section_text: str = "") -> Dict:
        """Runs complete education extraction pipeline."""
        target_text = education_section_text if len(education_section_text.strip()) > 30 else raw_text

        degrees = self.extract_degrees(raw_text)
        majors = self.extract_majors(raw_text)
        institutions = self.extract_institutions(target_text)
        gpa = self.extract_gpa(raw_text)

        highest_degree = degrees[0]["level"] if degrees else "None Detected"
        highest_rank = degrees[0]["rank"] if degrees else 0
        has_education = len(degrees) > 0 or len(institutions) > 0

        return {
            "has_education": has_education,
            "highest_degree_level": highest_degree,
            "degree_rank": highest_rank,
            "degrees_found": degrees,
            "majors_found": majors,
            "institutions_found": institutions,
            "gpa_or_grade": gpa
        }

