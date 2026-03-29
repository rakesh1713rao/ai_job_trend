from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
import re
from sqlalchemy import text
from app.database.db import engine
from collections import Counter


DOMAIN_STOPWORDS = [
    "apply", "build", "building", "built", "based",
    "deliver", "culture", "comfortable", "dedicated",
    "team", "role", "work", "years", "experience",
    "strong", "senior", "remote", "production", "hours",
    "small", "design", "ownership", "network", "infrastructure"
]

CUSTOM_STOPWORDS = list(ENGLISH_STOP_WORDS) + DOMAIN_STOPWORDS



SKILLS_LIST = [
    # Languages
    "python", "javascript", "typescript", "java", "ruby", "rust", "c++", "c#", "scala", "kotlin", "swift",
    # Web / Frameworks
    "react", "vue", "angular", "django", "fastapi", "flask", "rails", "next.js", "node.js", "express",
    # Data / ML / AI
    "machine learning", "deep learning", "nlp", "llm", "langchain", "pytorch", "tensorflow", "huggingface",
    "pandas", "numpy", "scikit-learn", "spark", "airflow", "dbt",
    # Cloud / DevOps
    "aws", "gcp", "azure", "docker", "kubernetes", "terraform", "ci/cd", "github actions", "linux",
    # Databases
    "sql", "postgresql", "postgres", "mysql", "mongodb", "redis", "elasticsearch", "sqlite",
    # Other tools
    "git", "rest api", "graphql", "kafka", "celery", "redis",
]


class TextCleaner(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        cleaned = []
        for text in X:
            text = text.lower()
            text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
            cleaned.append(text)
        return cleaned


def build_nlp_pipeline():
    pipeline = Pipeline([
        ("cleaner", TextCleaner()),
        ("tfidf", TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=100,
            stop_words= CUSTOM_STOPWORDS,
            max_df= 0.8

        ))
    ])
    return pipeline

def extract_skills(descriptions):
    """Match descriptions against known skills list and count occurrences."""
    skill_counter = Counter()

    for desc in descriptions:
        desc_lower = desc.lower()
        for skill in SKILLS_LIST:
            # Use word boundary to avoid false matches like "go to", "django" in "djangoproject"
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, desc_lower):
                skill_counter[skill] += 1

    return skill_counter


def get_job_descriptions():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT description FROM jobs"))
        rows = result.fetchall()

    return [row[0] for row in rows]