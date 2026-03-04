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
