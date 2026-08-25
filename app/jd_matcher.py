"""Job Description (JD) Matcher Module
Leverages TF-IDF vectorization and Cosine Similarity to score alignment against target job specs.
"""

import re
from typing import Dict, List, Set
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class JobDescriptionMatcher:
    """Calculates match score between candidate resume and target job description."""

    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words="english",
            max_features=500
        )

    def compute_similarity(self, resume_text: str, jd_text: str) -> float:
        """Computes cosine similarity percentage between resume and JD."""
        if not resume_text.strip() or not jd_text.strip():
            return 0.0

        try:
            tfidf_matrix = self.vectorizer.fit_transform([resume_text, jd_text])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            # Normalize to 0-100 percentage
            return round(float(similarity) * 100, 1)
        except Exception:
            return 0.0

    def extract_key_terms(self, text: str, top_n: int = 25) -> List[str]:
        """Extracts most important non-stopword technical and domain terms."""
        try:
            vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), max_features=100)
            vec.fit([text])
            feature_names = vec.get_feature_names_out()
            return [term for term in feature_names if len(term) > 2][:top_n]
        except Exception:
            words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
            return list(set(words))[:top_n]

    def match(self, resume_text: str, jd_text: str, resume_skills: List[str] = None) -> Dict:
        """Executes full alignment analysis between resume and JD."""
        if not jd_text.strip():
            return {
                "match_score": 0.0,
                "is_active": False,
                "matched_keywords": [],
                "missing_keywords": [],
                "match_level": "No JD Provided"
            }

        similarity_score = self.compute_similarity(resume_text, jd_text)
        jd_terms = self.extract_key_terms(jd_text, top_n=30)
        resume_lower = resume_text.lower()

        matched_terms: List[str] = []
        missing_terms: List[str] = []

        for term in jd_terms:
            if re.search(rf"\b{re.escape(term)}\b", resume_lower):
                matched_terms.append(term)
            else:
                missing_terms.append(term)

        # Keyword match ratio
        keyword_coverage = round(
            (len(matched_terms) / max(len(jd_terms), 1)) * 100, 1
        )

        # Blended Job Match Score
        blended_score = round((similarity_score * 0.5) + (keyword_coverage * 0.5), 1)

        if blended_score >= 70:
            match_level = "High Alignment (Strong Match)"
        elif blended_score >= 45:
            match_level = "Moderate Alignment (Good Match)"
        else:
            match_level = "Low Alignment (Missing Core Requirements)"

        return {
            "match_score": blended_score,
            "cosine_similarity": similarity_score,
            "keyword_coverage": keyword_coverage,
            "is_active": True,
            "match_level": match_level,
            "matched_keywords": matched_terms[:15],
            "missing_keywords": missing_terms[:15]
        }

