import requests
import time
from datetime import datetime
from textblob import TextBlob
import os
from dotenv import load_dotenv
load_dotenv() # Load secrets

# NO MORE HARDCODING
NYT_API_KEY = os.getenv("NYT_API_KEY")


def calculate_financial_sentiment(text):
    """
    Combines TextBlob (General English) with a Custom Financial Dictionary.
    """
    blob = TextBlob(text)
    base_score = blob.sentiment.polarity
    
    # Custom Financial Dictionary
    # TextBlob doesn't know that "profit" is good or "loss" is bad. We teach it.
    positive_terms = [
        "surge", "jump", "grow", "gain", "profit", "record", "high", "bull", 
        "optimis", "beat", "strong", "up", "rise", "vision", "success"
    ]
    negative_terms = [
        "drop", "fall", "decline", "loss", "miss", "bear", "fear", "weak", 
        "down", "crash", "slump", "fail", "risk", "uncertain", "cut"
    ]
    
    text_lower = text.lower()
    
    # Apply Boosts
    boost = 0.0
    for word in positive_terms:
        if word in text_lower:
            boost += 0.15  # Nudge score up
            
    for word in negative_terms:
        if word in text_lower:
            boost -= 0.15  # Nudge score down
            
    final_score = base_score + boost
    
    # Cap the score between -1 and 1
    return max(min(final_score, 1.0), -1.0)

def fetch_company_news(ticker, company_name):
    query = f"{company_name}"
    url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
    params = {
        "q": query,
        "api-key": NYT_API_KEY,
        "sort": "relevance",
        "fl": "headline,snippet,lead_paragraph,pub_date,web_url"
    }
    
    print(f"   [NYT] Searching for '{query}'...")
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            articles = response.json().get("response", {}).get("docs", [])
            cleaned_data = []
            
            for art in articles:
                headline = art.get("headline", {}).get("main", "")
                snippet = art.get("snippet", "") or ""
                lead_para = art.get("lead_paragraph", "") or ""
                
                full_text = f"{headline}. {snippet} {lead_para}"
                
                # USE NEW FUNCTION HERE
                score = calculate_financial_sentiment(full_text)
                
                doc = {
                    "related_ticker": ticker,
                    "source": "New York Times",
                    "title": headline,
                    "snippet": snippet,
                    "url": art.get("web_url"),
                    "published_at": art.get("pub_date"),
                    "fetched_at": datetime.utcnow(),
                    "sentiment_score": score
                }
                cleaned_data.append(doc)
            return cleaned_data
        else:
            print(f"   [ERROR] NYT Status: {response.status_code}")
            return []
    except Exception as e:
        print(f"   [ERROR] Connection failed: {e}")
        return []