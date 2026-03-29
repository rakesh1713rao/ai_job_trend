# 🤖 AI Job Trend Analyzer

A Python pipeline that scrapes real-world AI job postings, stores them in a local database, and uses NLP to extract and rank the most in-demand tech skills in the job market.

---

## 📌 What It Does

1. **Scrapes** job listings from the Remotive API
2. **Stores** them in a local SQLite database (with deduplication)
3. **Cleans** job descriptions using a custom NLP text cleaner
4. **Analyzes** descriptions using TF-IDF vectorization
5. **Extracts** in-demand skills using regex-based keyword matching
6. **Persists** skill data back into the database for querying

---

## 🗂️ Project Structure

```
ai_job_trend/
├── main.py                        # Entry point — runs the full pipeline
├── requirements.txt               # Python dependencies
├── .gitignore
└── app/
    ├── database/
    │   ├── db.py                  # SQLAlchemy engine setup (SQLite)
    │   ├── schema.py              # Table creation: jobs, skills, job_skills
    │   └── insert_jobs.py         # Insert, view, and link jobs to skills
    ├── scraper/
    │   └── api_client.py          # Fetches jobs from Remotive API
    └── nlp/
        └── ml_pipeline.py         # Text cleaning, TF-IDF, skill extraction
```

---

## 🗃️ Database Schema

### `jobs`
Stores scraped job postings. Duplicate jobs (same title + company) are automatically ignored.

| Column | Type | Description |
|---|---|---|
| id | INTEGER | Primary key |
| title | TEXT | Job title |
| company | TEXT | Company name |
| location | TEXT | Job location |
| description | TEXT | Full job description |
| posted_date | TEXT | Date posted |
| source | TEXT | Data source (e.g. Remotive_API) |
| scraped_date | TIMESTAMP | When it was scraped |

### `skills`
Master list of unique skill names found across all job postings.

### `job_skills`
Junction table linking jobs to the skills they mention.

---

## 🧠 NLP Pipeline

### Step 1 — Text Cleaning (`TextCleaner`)
A custom scikit-learn transformer that:
- Lowercases all text
- Strips special characters, unicode (`\xa0`), and emojis using regex
- Outputs clean, uniform strings ready for vectorization

### Step 2 — TF-IDF Vectorization
Converts cleaned descriptions into a numerical feature matrix.

- `ngram_range=(1, 2)` — captures single words and two-word phrases like "machine learning"
- `max_features=100` — keeps the top 100 most meaningful terms
- `stop_words` — filters out English stop words + custom domain noise words like `senior`, `remote`, `hours`, `production`
- `max_df=0.8` — ignores terms that appear in more than 80% of documents (too common to be meaningful)

> The TF-IDF matrix is kept for future use — job clustering, topic modeling, and similarity search.

### Step 3 — Skill Extraction (`extract_skills`)
Matches each job description against a curated list of 50+ known tech skills using **regex word boundary matching**.

```python
pattern = r'\b' + re.escape(skill) + r'\b'
```

This prevents false positives — e.g. `java` won't match inside `javascript`, and `sql` won't match inside `postgresql`.

Results are returned as a ranked `Counter` of skill frequencies.

---

## 🛠️ Skills Tracked

| Category | Skills |
|---|---|
| Languages | Python, JavaScript, TypeScript, Ruby, Rust, Scala, Kotlin, Swift, C++, C# |
| Web / Frameworks | React, Vue, Angular, Django, FastAPI, Flask, Rails, Next.js, Node.js, Express |
| Data / ML / AI | Machine Learning, Deep Learning, NLP, LLM, LangChain, PyTorch, TensorFlow, HuggingFace, Pandas, NumPy, Scikit-learn, Spark, Airflow, dbt |
| Cloud / DevOps | AWS, GCP, Azure, Docker, Kubernetes, Terraform, CI/CD, GitHub Actions, Linux |
| Databases | SQL, PostgreSQL, MySQL, MongoDB, Redis, Elasticsearch, SQLite |
| Other | Git, REST API, GraphQL, Kafka, Celery |

---

## ⚙️ Setup & Installation

```bash
# 1. Clone the repo
git clone https://github.com/rakesh1713rao/ai_job_trend.git
cd ai_job_trend

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the pipeline
python main.py
```

---

## 📊 Sample Output

```
✅ Jobs table created
✅ Skills tables ready
✅ Inserted 4 API Jobs

Feature matrix shape: (6, 100)

🔍 Top Skills in Job Market:
  kubernetes                2 job(s)
  nlp                       2 job(s)
  redis                     2 job(s)
  llm                       1 job(s)
  langchain                 1 job(s)
  python                    1 job(s)
  docker                    1 job(s)
  sql                       1 job(s)
  react                     1 job(s)
  postgresql                1 job(s)

✅ Job skills inserted
```

---

## 🐛 Known Issues & Fixes Applied

| Issue | Root Cause | Fix Applied |
|---|---|---|
| Garbled/repeating output | Incorrect print loop | Cleaned up pipeline output |
| Generic words as skills (`senior`, `remote`) | TF-IDF alone not suitable for skill extraction | Added curated keyword matching |
| False positives (`java` matching `javascript`) | Plain `in` string check | Switched to `\b` regex word boundaries |
| `go` matching "go to" (5 false hits) | Too generic a keyword | Removed `go`, use `golang` instead |
| Slow DB inserts | `conn.commit()` called inside loop | Moved commit outside the loop |
| Skills stored without word boundary check | `insert_job_skills` used plain `in` | Updated to use `re.search` with `\b` |

---

## 🚀 Roadmap

- [ ] Add more job sources (Adzuna, Jobicy, LinkedIn scraper)
- [ ] Schedule daily auto-scraping with APScheduler
- [ ] Build a skill trends dashboard (bar charts, time series)
- [ ] Use TF-IDF matrix for job clustering (KMeans)
- [ ] Add a job similarity / recommendation feature

---

## 🧰 Tech Stack

- **Python 3.x**
- **SQLAlchemy** — database ORM
- **SQLite** — local database
- **scikit-learn** — TF-IDF vectorization, custom transformers
- **Requests** — API calls to Remotive
- **Regex (re)** — text cleaning and skill matching

---

## 👤 Author

**Rakesh Rao**  
[github.com/rakesh1713rao](https://github.com/rakesh1713rao)
