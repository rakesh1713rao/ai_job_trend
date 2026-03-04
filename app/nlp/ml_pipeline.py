from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
import re
from sqlalchemy import text
from app.database.db import engine



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
            max_features=100
        ))
    ])
    return pipeline


def get_job_descriptions():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT description FROM jobs"))
        rows = result.fetchall()

    return [row[0] for row in rows]