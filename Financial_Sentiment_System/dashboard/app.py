from flask import Flask, render_template
from pymongo import MongoClient
import pandas as pd

app = Flask(__name__)
client = MongoClient("mongodb://mongodb:27017/")
db = client['sentiment_db']

def analyze_source(ticker, source_name):
    """
    Calculates sentiment and prediction for a SINGLE source (e.g., just NYT).
    """
    # 1. Fetch News for this specific source
    docs = list(db.news_data.find(
        {"related_ticker": ticker, "source": source_name}
    ).sort("published_at", -1).limit(3))
    
    # 2. Calculate Score
    avg_sentiment = 0
    if docs:
        avg_sentiment = sum(d.get('sentiment_score', 0) for d in docs) / len(docs)
    
    # 3. Determine "Mood" (Simplified for specific source comparison)
    prediction = "NEUTRAL"
    color = "orange"
    
    if avg_sentiment > 0.05:
        prediction = "BULLISH"
        color = "green"
    elif avg_sentiment < -0.05:
        prediction = "BEARISH"
        color = "red"
        
    return {
        "score": avg_sentiment,
        "prediction": prediction,
        "color": color,
        "news": docs
    }

@app.route('/')
def index():
    tickers = db.market_data.distinct("symbol")
    dashboard_data = []
    
    for ticker in tickers:
        # Get Price (Same for both)
        latest_price_doc = db.market_data.find_one({"symbol": ticker}, sort=[("timestamp", -1)])
        price = latest_price_doc['price'] if latest_price_doc else 0.0
        
        # Analyze separately
        nyt_data = analyze_source(ticker, "New York Times")
        api_data = analyze_source(ticker, "NewsAPI")
        
        dashboard_data.append({
            "ticker": ticker,
            "price": price,
            "nyt": nyt_data,   # The Institutional View
            "api": api_data    # The Public View
        })

    return render_template('index.html', data=dashboard_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)