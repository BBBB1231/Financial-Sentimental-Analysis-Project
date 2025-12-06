import requests
from datetime import datetime
from textblob import TextBlob
import os
from dotenv import load_dotenv
load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def fetch_generic_news(ticker, company_name):
    """
    Fetches news from the broader web using NewsAPI.
    """
    url = "https://newsapi.org/v2/everything"
    
    # We restrict to English and specific domains to avoid total junk
    params = {
        "q": company_name,
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 5  # Fetch top 5 per company
    }
    
    print(f"   [NewsAPI] Searching for '{company_name}'...")
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            articles = response.json().get("articles", [])
            cleaned_data = []
            
            for art in articles:
                title = art.get("title") or ""
                desc = art.get("description") or ""
                
                # Skip removed content
                if "[Removed]" in title: continue
                
                # Sentiment Analysis
                full_text = f"{title}. {desc}"
                blob = TextBlob(full_text)
                score = blob.sentiment.polarity
                
                doc = {
                    "related_ticker": ticker,
                    "source": "NewsAPI",  # <--- Tagging the Source
                    "source_name": art.get("source", {}).get("name", "Unknown"),
                    "title": title,
                    "snippet": desc,
                    "url": art.get("url"),
                    "published_at": art.get("publishedAt"),
                    "fetched_at": datetime.utcnow(),
                    "sentiment_score": score
                }
                cleaned_data.append(doc)
            return cleaned_data
        else:
            print(f"   [NewsAPI] Error: {response.status_code}")
            return []
    except Exception as e:
        print(f"   [NewsAPI] Connection failed: {e}")
        return []