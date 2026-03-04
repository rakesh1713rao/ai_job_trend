from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///ai_jobs.db"

engine = create_engine(DATABASE_URL, echo=True)