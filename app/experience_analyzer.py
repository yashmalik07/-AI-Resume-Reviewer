"""Experience & Impact Analyzer Module
Analyzes years of experience, action verbs, quantified metrics, and seniority level.
"""

import re
from datetime import datetime
from typing import Dict, List, Set, Tuple


class ExperienceAnalyzer:
    """Analyzes work history, depth of impact, metrics, and action verbs."""

    STRONG_ACTION_VERBS = [
        "architected", "engineered", "spearheaded", "orchestrated", "developed",
        "optimized", "streamlined", "implemented", "accelerated", "scaled",
        "deployed", "designed", "constructed", "built", "modernized", "refactored",
        "delivered", "formulated", "pioneered", "mentored", "championed",
        "resolved", "maximized", "minimized", "automated", "transformed", "generated"
    ]

    WEAK_PASSIVE_PHRASES = [
        "responsible for", "duties included", "worked on", "helped with",
        "assisted in", "participated in", "tasked with", "handled", "did",
        "was part of"
    ]

    EXPERIENCE_PATTERNS = [
        r"(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)(?:\s+of)?\s+(?:experience|work)",
        r"(?:experience|work\s+history)\s*:\s*(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)",
        r"(?:over|more\s+than)\s+(\d+(?:\.\d+)?)\s*(?:years?|yrs?)",
        r"(\d+(?:\.\d+)?)\s*\+\s*years?"
    ]

    # Regex pattern for date ranges like "2020 - 2023", "Jan 2021 - Present", "06/2019 - 08/2022"
    DATE_RANGE_PATTERN = r"(?:(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+)?(20\d{2}|19\d{2})\s*(?:-|–|to)\s*(?:(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+)?(20\d{2}|19\d{2}|present|current|now)"

    # Metric & quantification pattern ($100k, 40%, 10k users, 5x speedup, 15+ engineers)
    METRIC_PATTERN = r"(?:\$\d+(?:\.\d+)?\s*[kKmMbB]?|\d+(?:\.\d+)?%|\b\d+\s*(?:x|times|fold)\b|\b\d+\+?\s*(?:users|clients|customers|requests|queries|rps|team\s+members|engineers|models|pipelines)\b)"

    def __init__(self):
        self.current_year = datetime.now().year

    def extract_years_of_experience(self, text: str) -> float:
        """Extracts total estimated years of experience from text and date ranges."""
        extracted_years = 0.0

        # 1. Direct explicit statements
        for pattern in self.EXPERIENCE_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for m in matches:
                try:
                    val = float(m)
                    if 0 < val < 50:
                        extracted_years = max(extracted_years, val)
                except ValueError:
                    continue

        # 2. Date ranges calculation
        date_matches = re.findall(self.DATE_RANGE_PATTERN, text, re.IGNORECASE)
        calculated_years = 0.0
        seen_ranges: Set[Tuple[int, int]] = set()

        for start_str, end_str in date_matches:
            try:
                start_year = int(start_str)
                if end_str.lower() in ["present", "current", "now"]:
                    end_year = self.current_year
                else:
                    end_year = int(end_str)

                if 1980 <= start_year <= self.current_year and start_year <= end_year <= self.current_year + 1:
                    year_span = max(end_year - start_year, 0.5)
                    if (start_year, end_year) not in seen_ranges:
                        seen_ranges.add((start_year, end_year))
                        calculated_years += year_span
            except Exception:
                continue

        # Use maximum credible value
        final_years = max(extracted_years, calculated_years)
        return min(round(final_years, 1), 40.0)

    def analyze_action_verbs(self, text: str) -> Dict:
        """Identifies strong action verbs and weak passive phrases used in bullet points."""
        text_lower = text.lower()

        found_strong: List[str] = []
        for verb in self.STRONG_ACTION_VERBS:
            if re.search(rf"\b{re.escape(verb)}\b", text_lower):
                found_strong.append(verb)

        found_weak: List[str] = []
        for phrase in self.WEAK_PASSIVE_PHRASES:
            if re.search(rf"\b{re.escape(phrase)}\b", text_lower):
                found_weak.append(phrase)

        return {
            "strong_verbs_count": len(found_strong),
            "strong_verbs": found_strong,
            "weak_phrases_count": len(found_weak),
            "weak_phrases": found_weak,
            "verb_strength_ratio": round(
                len(found_strong) / max(len(found_strong) + len(found_weak), 1), 2
            )
        }

    def detect_quantified_metrics(self, text: str) -> List[str]:
        """Detects presence of measurable results, percentages, and metrics."""
        matches = re.findall(self.METRIC_PATTERN, text, re.IGNORECASE)
        # Clean and deduplicate while preserving order
        seen = set()
        deduped = []
        for m in matches:
            clean_m = m.strip()
            if clean_m.lower() not in seen:
                seen.add(clean_m.lower())
                deduped.append(clean_m)
        return deduped

    def determine_seniority(self, years: float, text: str) -> str:
        """Determines candidate seniority level based on tenure and role titles."""
        text_lower = text.lower()

        if re.search(r"\b(?:lead|principal|architect|director|head of|vp|chief)\b", text_lower) or years >= 8:
            return "Senior / Lead"
        elif re.search(r"\b(?:senior|sr\.?|staff)\b", text_lower) or years >= 5:
            return "Mid-Senior"
        elif years >= 2:
            return "Mid-Level"
        elif re.search(r"\b(?:intern|trainee|fresher|entry[- ]level|junior|jr\.?)\b", text_lower) or years < 2:
            return "Entry-Level / Intern"
        return "Mid-Level"

    def analyze(self, raw_text: str, experience_section_text: str = "") -> Dict:
        """Runs full experience analysis pipeline."""
        target_text = experience_section_text if len(experience_section_text.strip()) > 50 else raw_text

        years = self.extract_years_of_experience(raw_text)
        action_verbs = self.analyze_action_verbs(target_text)
        metrics = self.detect_quantified_metrics(target_text)
        seniority = self.determine_seniority(years, raw_text)

        # Experience relevance signals
        exp_keywords = [
            "experience", "worked", "developed", "managed", "led", "designed",
            "implemented", "engineered", "built", "delivered", "coordinated"
        ]
        keyword_hits = sum(1 for kw in exp_keywords if re.search(rf"\b{kw}\b", raw_text.lower()))

        has_experience = (years > 0) or (len(metrics) > 0) or (keyword_hits >= 3)

        return {
            "years": years,
            "has_experience": has_experience,
            "seniority_level": seniority,
            "action_verbs": action_verbs,
            "quantified_metrics": metrics,
            "metrics_count": len(metrics),
            "experience_keyword_hits": keyword_hits
        }

