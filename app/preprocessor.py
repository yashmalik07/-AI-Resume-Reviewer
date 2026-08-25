"""NLP Text Preprocessor and Section Segmenter
Cleans raw text, tokenizes, lemmatizes, and segments resumes into logical sections.
"""

import re
from typing import Dict, List, Tuple
import nltk

# Ensure standard NLTK resources are available with quiet fallback
for resource in ["punkt", "stopwords", "wordnet", "punkt_tab"]:
    try:
        nltk.data.find(f"tokenizers/{resource}" if "punkt" in resource else f"corpora/{resource}")
    except LookupError:
        try:
            nltk.download(resource, quiet=True)
        except Exception:
            pass

try:
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    STOP_WORDS = set(stopwords.words("english"))
    LEMMATIZER = WordNetLemmatizer()
except Exception:
    STOP_WORDS = {
        "i", "me", "my", "myself", "we", "our", "ours", "you", "your", "he", "she",
        "it", "they", "them", "what", "which", "who", "whom", "this", "that", "these",
        "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has",
        "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but",
        "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with",
        "about", "against", "between", "into", "through", "during", "before", "after",
        "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over",
        "under", "again", "further", "then", "once", "here", "there", "when", "where",
        "why", "how", "all", "any", "both", "each", "few", "more", "most", "other",
        "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too",
        "very", "can", "will", "just", "don", "should", "now"
    }
    class SimpleLemmatizer:
        def lemmatize(self, word):
            if word.endswith("ing") and len(word) > 5:
                return word[:-3]
            if word.endswith("ed") and len(word) > 4:
                return word[:-2]
            if word.endswith("s") and len(word) > 3:
                return word[:-1]
            return word
    LEMMATIZER = SimpleLemmatizer()


class TextPreprocessor:
    """Handles text normalization, tokenization, and section parsing."""

    SECTION_HEADERS = {
        "summary": [
            r"summary", r"professional\s+summary", r"profile", r"about\s+me",
            r"objective", r"career\s+objective", r"executive\s+summary"
        ],
        "experience": [
            r"experience", r"work\s+experience", r"professional\s+experience",
            r"employment\s+history", r"work\s+history", r"internships",
            r"relevant\s+experience"
        ],
        "education": [
            r"education", r"academic\s+background", r"academic\s+history",
            r"qualifications", r"educational\s+qualifications"
        ],
        "skills": [
            r"skills", r"technical\s+skills", r"core\s+competencies",
            r"technologies", r"areas\s+of\s+expertise", r"key\s+skills"
        ],
        "projects": [
            r"projects", r"personal\s+projects", r"academic\s+projects",
            r"key\s+projects", r"portfolio"
        ],
        "certifications": [
            r"certifications", r"licenses", r"credentials",
            r"courses\s+and\s+certifications", r"training"
        ],
        "awards": [
            r"awards", r"honors", r"achievements", r"accomplishments",
            r"extracurricular"
        ]
    }

    def __init__(self):
        self.stop_words = STOP_WORDS
        self.lemmatizer = LEMMATIZER

    def clean_text(self, text: str) -> str:
        """Basic text cleaning: handles encoding artifacts, whitespaces, and tabs."""
        if not text:
            return ""
        # Normalize line endings
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        # Remove unusual unicode control chars
        text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]", " ", text)
        # Normalize spaces
        text = re.sub(r"[ \t]+", " ", text)
        return text.strip()

    def tokenize_and_lemmatize(self, text: str) -> Tuple[str, List[str]]:
        """Normalize, strip punctuation, remove stopwords, and lemmatize tokens."""
        cleaned = text.lower()
        # Keep letters, numbers, and basic code symbols
        cleaned = re.sub(r"[^a-zA-Z0-9\s\+\#\.\-]", " ", cleaned)
        try:
            tokens = nltk.word_tokenize(cleaned)
        except Exception:
            tokens = cleaned.split()

        processed_tokens = []
        for token in tokens:
            token_clean = token.strip(".-")
            if token_clean and token_clean not in self.stop_words and len(token_clean) > 1:
                try:
                    lemmatized = self.lemmatizer.lemmatize(token_clean)
                except Exception:
                    lemmatized = token_clean
                processed_tokens.append(lemmatized)

        return " ".join(processed_tokens), processed_tokens

    def get_text_statistics(self, raw_text: str) -> Dict:
        """Compute structural metrics like word count, lines, and reading ease."""
        words = raw_text.split()
        word_count = len(words)
        lines = [line.strip() for line in raw_text.split("\n") if line.strip()]
        line_count = len(lines)
        
        # Estimate sentence count
        sentences = re.split(r"[.!?]+", raw_text)
        sentence_count = len([s for s in sentences if len(s.strip()) > 3])

        avg_words_per_line = word_count / max(line_count, 1)

        return {
            "word_count": word_count,
            "line_count": line_count,
            "sentence_count": max(sentence_count, 1),
            "char_count": len(raw_text),
            "avg_words_per_line": round(avg_words_per_line, 2)
        }

    def segment_sections(self, text: str) -> Dict[str, str]:
        """Segments raw resume text into distinct functional sections."""
        lines = text.split("\n")
        sections: Dict[str, List[str]] = {key: [] for key in self.SECTION_HEADERS}
        sections["header"] = []
        sections["other"] = []

        current_section = "header"

        for line in lines:
            trimmed = line.strip()
            if not trimmed:
                continue

            # Check if this line is likely a section header (short line, matches regex)
            is_header = False
            if len(trimmed.split()) <= 4:
                line_lower = trimmed.lower().strip(":#*- ")
                for sec_name, patterns in self.SECTION_HEADERS.items():
                    for pattern in patterns:
                        if re.fullmatch(pattern, line_lower) or line_lower == pattern.replace(r"\s+", " "):
                            current_section = sec_name
                            is_header = True
                            break
                    if is_header:
                        break

            if not is_header:
                if current_section in sections:
                    sections[current_section].append(trimmed)
                else:
                    sections["other"].append(trimmed)

        # Join lines into unified text blocks
        return {sec: "\n".join(content) for sec, content in sections.items()}

