# AlphaSignal: Financial Market Sentiment Intelligence System

### Group 9 Term Project
**Course:** 5400 - Big Data Analytics  
**Status:** Final Submission

---

## Project Overview
AlphaSignal is a real-time data engineering pipeline that analyzes financial sentiment divergence between institutional news (New York Times) and public sentiment (NewsAPI/General Web).

The system continuously ingests news articles, applies Natural Language Processing (TextBlob) to calculate sentiment scores (-1 to +1), and visualizes the data on a live Flask dashboard.

## System Architecture
This project utilizes a **Microservices Architecture** orchestrated by Docker.

* ** ETL Service (Python):** Continuously polls NYT and NewsAPI, cleans data, calculates sentiment, and upserts to MongoDB.
* ** Database Service (MongoDB):** A NoSQL document store that handles the unstructured news data.
* ** Dashboard Service (Flask):** A web application that queries the database and serves a real-time analytics interface.

---

##  Technologies Used
* **Containerization:** Docker & Docker Compose
* **Database:** MongoDB (NoSQL)
* **Backend/Frontend:** Python, Flask, HTML/CSS
* **Data Processing:** Pandas, TextBlob, Pymongo
* **External APIs:**
    * New York Times API
    * NewsAPI
    * Yahoo Finance (`yfinance`)

---

##  How to Replicate This Project

### 1. Prerequisites
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
* Git installed.

### 2. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/financial-sentiment-system.git](https://github.com/YOUR_USERNAME/financial-sentiment-system.git)
cd financial-sentiment-system
```

### 3. API Key Setup (Crucial!)
For security, API keys are **not** stored in this repository. You must create a `.env` file locally.

1.  Create a file named `.env` in the root folder.
2.  Add your keys in the following format:

```ini
# .env file
NYT_API_KEY=your_nyt_key_here
NEWS_API_KEY=your_newsapi_key_here
MONGO_URI=mongodb://mongo:27017/
```

### 4. Run the Application
We use Docker Compose to spin up the entire pipeline with one command:
```bash
docker-compose up --build
```
What happens next:

Docker builds the ETL and Dashboard containers.

MongoDB starts immediately.

The ETL pipeline begins fetching news articles every 60 seconds.

The Dashboard launches.


### 5. Access the Dashboard

Open your web browser and navigate to: http://localhost:5000

===================================================================
===================================================================
### Project Structure

├── financial_sentiment_system/
│   ├── etl_pipeline/        # Scraper & Sentiment Logic
│   ├── dashboard/           # Flask App & Templates
│   ├── docker-compose.yml   # Orchestration
├── submission.ipynb         # Data Analysis Demo & Architecture
├── README.md                # Documentation
└── .gitignore               # Security rules
