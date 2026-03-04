from sqlalchemy import text
from app.database.db import engine

def create_jobs_table():
    with engine.connect() as conn:
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            company TEXT,
            location TEXT,
            description TEXT,
            posted_date TEXT,
            source TEXT,
            scraped_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(title, company)
        )
        """))
        conn.commit()
        print("✅ Jobs table created")

def create_skills_tables():
    with engine.connect() as conn:
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
        """))

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS job_skills (
            job_id INTEGER,
            skill_id INTEGER,
            PRIMARY KEY (job_id, skill_id),
            FOREIGN KEY(job_id) REFERENCES jobs(id),
            FOREIGN KEY(skill_id) REFERENCES skills(id)
        )
        """))

        conn.commit()

    print("✅ Skills tables ready")

if __name__ == "__main__":
    create_jobs_table()