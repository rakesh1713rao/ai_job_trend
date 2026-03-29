from app.database.schema import create_jobs_table, create_skills_tables
from app.database.insert_jobs import insert_api_jobs, view_jobs, insert_job_skills
from app.nlp.ml_pipeline import build_nlp_pipeline, get_job_descriptions,extract_skills
from app.nlp.skill_dictionary import SKILLS
import numpy as np

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

        # Skill extraction
        skill_counts = extract_skills(descriptions)
        print("\n🔍 Top Skills in Job Market:")
        for skill, count in skill_counts.most_common(20):
            print(f"  {skill:<25} {count} job(s)")
    else:
        print("No job descriptions found.")        

        # feature_names = pipeline.named_steps["tfidf"].get_feature_names_out()

        # # 🔥 IMPORTANT: Calculate top terms
        # scores = np.asarray(X.mean(axis=0)).ravel()
        # top_indices = scores.argsort()[-20:][::-1]

        # print("\nTop TF-IDF Terms:")
        # for i in top_indices:
        #     print(feature_names[i])

        # # 🔥 Skill filtering
        # print("\nFiltered Skills:")
        # for i in top_indices:
        #     term = feature_names[i]

        #     if term in SKILLS:
        #         print(term)

    # else:
    #     print("No job descriptions found.")

