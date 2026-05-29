# AI Resume Analyzer Pro

AI Resume Analyzer Pro is an intelligent resume screening and candidate evaluation platform that helps job seekers optimize their resumes while providing recruiters with actionable hiring insights. The system leverages Natural Language Processing (NLP), Machine Learning, ATS-style scoring, semantic similarity analysis, and recruiter analytics to evaluate resumes against job descriptions.

---

## Features

### Resume Processing
- Upload resumes in PDF format
- Extract raw text from resumes
- NLP-based text preprocessing and cleaning
- Automatic contact information extraction

### Resume Intelligence
- Skill extraction from resumes
- Resume section identification
- Career field prediction
- Candidate classification
- ATS-style resume scoring
- Resume quality evaluation

### Job Matching
- Job description analysis
- Semantic similarity matching
- Resume-to-job compatibility scoring
- Skill gap identification
- Job match percentage calculation

### Career Recommendations
- Recommended technical skills
- Career field suggestions
- Learning path recommendations
- Suggested certification courses

### Recruiter Analytics Dashboard
- Resume analysis history
- Candidate distribution analytics
- Resume score analytics
- Predicted field visualization
- Candidate classification insights
- Feedback tracking system

### User Feedback System
- Collect user feedback
- Track user experience ratings
- Store recruiter and candidate feedback
- Dashboard analytics for feedback trends

---

## Screenshots

### User Dashboard
- Resume upload
- ATS scoring
- Job matching
- Candidate insights

### Admin Dashboard
- Analytics dashboard
- Candidate distribution charts
- Resume scoring insights
- Feedback analytics

---

## Technology Stack

### Frontend
- Streamlit

### Backend
- Python

### Machine Learning & NLP
- Scikit-Learn
- TF-IDF Vectorization
- Cosine Similarity
- Feature Engineering
- K-Means Clustering

### Data Processing
- Pandas
- NumPy

### Database
- SQLite

### Visualization
- Plotly
- Plotly Express

### Resume Parsing
- PyPDF2

---

## Project Architecture

```text
AI-Resume-Analyzer/
│
├── app.py
│
├── data/
│   ├── field_config.py
│   ├── courses.py
│   └── skills.py
│
├── src/
│   ├── parser.py
│   ├── preprocess.py
│   ├── extractor.py
│   ├── predictor.py
│   ├── scorer.py
│   ├── recommender.py
│   ├── database.py
│   └── analytics.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Machine Learning Pipeline

### Step 1: Resume Parsing
- Extract text from PDF resumes
- Convert resume into machine-readable format

### Step 2: NLP Preprocessing
- Lowercasing
- Tokenization
- Stopword removal
- Text normalization

### Step 3: Information Extraction
- Email extraction
- Phone number extraction
- Skill extraction
- Section detection

### Step 4: Feature Engineering
- Resume feature creation
- Skill-based profiling
- Section completeness analysis

### Step 5: Semantic Similarity
- TF-IDF vectorization
- Resume embedding generation
- Job description embedding generation
- Cosine similarity calculation

### Step 6: ATS Resume Scoring
Evaluation factors include:

- Skill coverage
- Resume completeness
- Project presence
- Experience section
- Education section
- Certifications section
- Job description alignment

### Step 7: Career Field Prediction
Fields supported:

- Data Science
- Machine Learning
- Artificial Intelligence
- Software Engineering
- Web Development
- Backend Development
- Frontend Development
- Cloud Computing
- DevOps
- Cybersecurity
- Business Intelligence
- Database Engineering

### Step 8: Candidate Classification

Categories:

- Excellent Fit
- Strong Fit
- Moderate Fit
- Weak Fit
- Poor Fit

---

## Installation

### Clone Repository

```bash
git clone https://github.com/Harsha85018/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Mac/Linux:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Application

```bash
streamlit run app.py
```

Application launches at:

```text
http://localhost:8501
```

---

## Admin Dashboard

The Admin Dashboard provides:

### Resume Analytics
- Total resume analyses
- Average resume score
- Candidate classification distribution
- Predicted field distribution

### Candidate Insights
- Candidate records
- Resume metadata
- Skill profiles
- Career recommendations

### Feedback Analytics
- User ratings
- User comments
- Feedback summaries

---

## Sample Workflow

1. Upload Resume PDF
2. Paste Job Description
3. Click Analyze Resume
4. View:
   - ATS Score
   - Job Match Score
   - Candidate Classification
   - Career Field Prediction
   - Recommended Skills
   - Recommended Courses
5. Review Recruiter Analytics

---

## Future Enhancements

### Planned Improvements

- Sentence Transformers Embeddings
- BERT-based Resume Matching
- OpenAI-powered Resume Feedback
- Resume Ranking System
- Multiple Resume Comparison
- Recruiter Authentication
- PDF Report Generation
- Cloud Deployment
- Docker Support
- REST API Integration
- Resume Keyword Optimization
- LLM-powered Career Recommendations

---

## Resume Highlights

### Key Features Demonstrated

- Natural Language Processing
- Machine Learning
- Semantic Search
- ATS Scoring
- Feature Engineering
- Data Visualization
- Database Management
- Dashboard Development
- End-to-End ML Application Development

---

## Author

**Harshavardhan Reddy Kaditham**

Master of Science in Data Science  
Indiana University Bloomington

GitHub: https://github.com/Harsha85018

LinkedIn: https://linkedin.com/in/harsha-kaditham

---

## License

This project is intended for educational, research, and portfolio purposes.
