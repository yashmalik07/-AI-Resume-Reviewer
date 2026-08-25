"""Skill Extraction and Categorization Module
Extracts technical, cloud, data science, web, database, and soft skills using taxonomy & n-gram matching.
"""

import re
from typing import Dict, List, Set


class SkillExtractor:
    """Extracts and categorizes technical and soft skills from resume text."""

    TECHNICAL_SKILL_TAXONOMY = {
        "programming": [
            "python", "java", "javascript", "typescript", "c++", "c#", "c",
            "golang", "go", "rust", "ruby", "php", "swift", "kotlin",
            "scala", "dart", "r", "julia", "matlab", "bash", "shell", "powershell"
        ],
        "data_science_ai": [
            "machine learning", "deep learning", "nlp", "natural language processing",
            "computer vision", "generative ai", "large language models", "llms",
            "tensorflow", "pytorch", "keras", "scikit-learn", "sklearn",
            "pandas", "numpy", "scipy", "matplotlib", "seaborn", "spacy", "nltk",
            "hugging face", "transformers", "opencv", "langchain", "llamaindex",
            "xgboost", "lightgbm", "catboost", "statistics", "data analysis",
            "data visualization", "feature engineering", "neural networks"
        ],
        "web_development": [
            "html", "html5", "css", "css3", "sass", "tailwind css", "bootstrap",
            "react", "react.js", "angular", "vue", "vue.js", "next.js", "nuxt.js",
            "node.js", "express.js", "express", "django", "flask", "fastapi",
            "spring boot", "asp.net", "graphql", "rest api", "restful apis",
            "websockets", "redux", "svelte"
        ],
        "cloud_devops": [
            "aws", "amazon web services", "gcp", "google cloud platform",
            "azure", "microsoft azure", "docker", "kubernetes", "k8s",
            "terraform", "ansible", "jenkins", "github actions", "gitlab ci",
            "ci/cd", "continuous integration", "continuous deployment",
            "linux", "serverless", "microservices", "helm", "prometheus", "grafana"
        ],
        "databases": [
            "sql", "mysql", "postgresql", "postgres", "mongodb", "redis",
            "sqlite", "cassandra", "oracle", "snowflake", "bigquery",
            "dynamodb", "elasticsearch", "neo4j", "mariadb", "firebase"
        ],
        "tools_methodologies": [
            "git", "github", "gitlab", "jira", "confluence", "agile",
            "scrum", "kanban", "test driven development", "tdd", "postman",
            "pytest", "unittest", "selenium", "webpack", "vite", "tableau", "power bi"
        ]
    }

    SOFT_SKILLS = [
        "communication", "teamwork", "leadership", "problem solving",
        "critical thinking", "time management", "adaptability", "collaboration",
        "conflict resolution", "mentorship", "creativity", "presentation skills",
        "analytical thinking", "work ethic", "decision making", "agile mindset",
        "interpersonal skills", "negotiation", "ownership", "multitasking"
    ]

    # Single-letter or ambiguous short keywords that need special boundary handling
    AMBIGUOUS_SKILLS = {"c", "r", "go"}

    def __init__(self):
        # Flatten all technical skills for fast lookup
        self.all_tech_skills: Dict[str, str] = {}
        for category, skills in self.TECHNICAL_SKILL_TAXONOMY.items():
            for skill in skills:
                self.all_tech_skills[skill.lower()] = category

    def _match_skill(self, skill: str, text: str, lower_text: str) -> bool:
        """Accurately match skills avoiding substring false positives."""
        skill_lower = skill.lower()
        if skill_lower in self.AMBIGUOUS_SKILLS:
            # Require distinct word boundaries or programming context
            pattern = rf"(?:\b|[\s,/]){re.escape(skill_lower)}(?:[\s,/]|\b)"
            if re.search(pattern, lower_text):
                # Extra check: make sure programming / language is in context
                return bool(re.search(rf"\b(?:programming|language|code|dev|skills?|c/c\+\+|in\s+{skill_lower})\b", lower_text))
            return False

        # If multi-word skill, simple phrase search
        if " " in skill_lower or "." in skill_lower or "+" in skill_lower or "#" in skill_lower:
            escaped = re.escape(skill_lower)
            return bool(re.search(rf"(?<![a-z0-9]){escaped}(?![a-z0-9])", lower_text))

        # Standard single word skill with word boundary
        pattern = rf"\b{re.escape(skill_lower)}\b"
        return bool(re.search(pattern, lower_text))

    def extract_skills(self, raw_text: str) -> Dict:
        """Extracts and categorizes technical and soft skills with metrics."""
        cleaned_lower = raw_text.lower()

        found_tech_by_category: Dict[str, List[str]] = {
            cat: [] for cat in self.TECHNICAL_SKILL_TAXONOMY
        }
        all_tech_found: Set[str] = set()
        soft_skills_found: Set[str] = set()

        # Match technical skills
        for category, skills in self.TECHNICAL_SKILL_TAXONOMY.items():
            for skill in skills:
                if self._match_skill(skill, raw_text, cleaned_lower):
                    normalized = skill.title() if len(skill) > 3 else skill.upper()
                    if skill.lower() in ["nlp", "aws", "gcp", "sql", "html", "css", "ci/cd", "tdd", "llms"]:
                        normalized = skill.upper()
                    found_tech_by_category[category].append(normalized)
                    all_tech_found.add(normalized)

        # Match soft skills
        for soft_skill in self.SOFT_SKILLS:
            if self._match_skill(soft_skill, raw_text, cleaned_lower):
                soft_skills_found.add(soft_skill.title())

        # Skill diversity and distribution
        total_tech_count = len(all_tech_found)
        total_soft_count = len(soft_skills_found)
        total_skills_count = total_tech_count + total_soft_count

        active_categories = [cat for cat, items in found_tech_by_category.items() if len(items) > 0]
        diversity_ratio = len(active_categories) / len(self.TECHNICAL_SKILL_TAXONOMY)

        return {
            "categorized_technical": found_tech_by_category,
            "all_technical": sorted(list(all_tech_found)),
            "soft_skills": sorted(list(soft_skills_found)),
            "technical_count": total_tech_count,
            "soft_count": total_soft_count,
            "total_skills_count": total_skills_count,
            "category_coverage": {
                cat: len(items) for cat, items in found_tech_by_category.items()
            },
            "diversity_ratio": round(diversity_ratio, 2)
        }

