import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup

def clean_html(text):
  return BeautifulSoup(text, "html.parser").get_text()



def fetch_remotive_jobs(keyword="AI"):
  url = "https://remotive.com/api/remote-jobs"

  response = requests.get(url)

  if response.status_code != 200:
    print("❌ API Error:", response.status_code)
    return []
  
  data = response.json()

  jobs = []

  for job in data.get("jobs", []):
    title = job.get("title","").lower()

    # location = job.get("candidate_required_location","").lower()

    if (
      any(k in title for k in ["ai", "ml", "machine learning", "data scientist"])
      # and ("india" in location or "anywhere" in location)
    ):
      jobs.append({
        "title": job.get("title"),
        "company": job.get("company_name"),
        "location": job.get("candidate_required_location"),
        "description": clean_html(job.get("description","")),
        "posted_date": job.get("publication_date"),
        "source": "Remotive_API"
      })

  # print(f"Fetched {len(jobs)} AI-related jobs")
  return jobs


"""
load_dotenv()
APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

def fetch_adzuna_jobs(keywords='AI Engineer', location= "India", page=1):
  url = f"https://api.adzuna.com/v1/api/jobs/in/search/{page}"

  params = {
    "app_id": APP_ID,
    "app_key": APP_KEY,
    "where": location,
    "result_per_page":20,
    "content-type":"application/json"

  }

  response = requests.get(url=url,params=params)

  if response.status_code != 200:
    print("❌ API Error:",response.status_code,response.text)
    return []
  
  data = response.json()

  jobs = []

  for job in data.get("results",[]):
    jobs.append({
      "title":job.get("title"),
      "company":job.get("company",{}).get("display_name"),
      "location":job.get("loaction",{}).get("display_name"),
      "description":job.get("description"),
      "posted_date":job.get("created"),
      "source":"ADZUNA_API"

    })

    return jobs

"""