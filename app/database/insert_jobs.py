from sqlalchemy import text
from app.database.db import engine
from app.scraper.api_client import fetch_remotive_jobs


def insert_sample_job():
    with engine.connect() as conn:
        conn.execute(text("""
        INSERT OR IGNORE INTO jobs (title, company, location, description, posted_date)
        VALUES (:title, :company, :location, :description, :posted_date)
        """), {
            "title": "AI Engineer",
            "company": "OpenAI Labs",
            "location": "Remote",
            "description": "Looking for experience with PyTorch, LangChain, and AWS.",
            "posted_date": "2026-03-01"
        })
        conn.commit()

    print("✅ Sample job inserted")


def view_jobs():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM jobs"))
        rows = result.fetchall()

        for row in rows:
            print(row)


def insert_api_jobs():
    jobs = fetch_remotive_jobs()

    if not jobs:
        print("NO Jobs Fetch From API")
        return
    
    with engine.connect() as conn:
        for job in jobs:
            conn.execute(text("""
                    INSERT OR IGNORE INTO jobs (title, company, location, description, posted_date, source)
                    VALUES (:title, :company, :location, :description, :posted_date, :source)
                    """), job)
            
        conn.commit()
          
    print(f" Inserted {len(jobs)} API Jobs ")


def insert_job_skills(skill_counts):
    """Store extracted skill frequencies into the skills and job_skills tables."""
    with engine.connect() as conn:
        for skill in skill_counts.keys():
            # Insert skill if it doesn't exist
            conn.execute(text("""
                INSERT OR IGNORE INTO skills (name) VALUES (:name)
            """), {"name": skill})
        conn.commit()

        # Now link jobs to skills
        jobs = conn.execute(text("SELECT id, description FROM jobs")).fetchall()
        
        from app.nlp.ml_pipeline import SKILLS_LIST
        for job_id, description in jobs:
            desc_lower = description.lower()
            for skill in SKILLS_LIST:
                if skill in desc_lower:
                    # Get skill id
                    skill_row = conn.execute(
                        text("SELECT id FROM skills WHERE name = :name"),
                        {"name": skill}
                    ).fetchone()
                    
                    if skill_row:
                        conn.execute(text("""
                            INSERT OR IGNORE INTO job_skills (job_id, skill_id)
                            VALUES (:job_id, :skill_id)
                        """), {"job_id": job_id, "skill_id": skill_row[0]})
        
        conn.commit()
    print("✅ Job skills inserted")
