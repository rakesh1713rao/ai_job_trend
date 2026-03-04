from app.database.schema import create_jobs_table, create_skills_tables
from app.database.insert_jobs import insert_api_jobs, view_jobs
from app.nlp.ml_pipeline import build_nlp_pipeline, get_job_descriptions


if __name__ == "__main__":
    create_jobs_table()
    create_skills_tables()
    insert_api_jobs()
    view_jobs()


    descriptions = get_job_descriptions()
    
    if descriptions:
        pipeline = build_nlp_pipeline()
        X = pipeline.fit_transform(descriptions)

        print("Feature matrix shape:", X.shape)
    else:
        print("No job descriptions found.")