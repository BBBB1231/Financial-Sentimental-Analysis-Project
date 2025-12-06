import time
import pymongo
import yfinance as yf
# Import BOTH collectors
from collectors.nyt_news import fetch_company_news as fetch_nyt
from collectors.generic_news import fetch_generic_news as fetch_newsapi

DB_URI = "mongodb://mongodb:27017/"

TARGETS = [
    {"symbol": "AAPL", "name": "Apple Inc"},
    {"symbol": "TSLA", "name": "Tesla Inc"},
    {"symbol": "NVDA", "name": "Nvidia"},
    {"symbol": "SPY",  "name": "Stock Market"}
]

def run_pipeline():
    print("--- STARTING DUAL-SOURCE INTELLIGENCE PIPELINE ---")
    client = pymongo.MongoClient(DB_URI)
    db = client["sentiment_db"]
    market_col = db["market_data"]
    news_col = db["news_data"]

    # Ensure URLs are unique so we don't save duplicates
    news_col.create_index("url", unique=True)

    while True:
        print("\n--- NEW CYCLE STARTED ---")
        
        for target in TARGETS:
            ticker = target["symbol"]
            name = target["name"]
            
            # 1. MARKET DATA
            try:
                stock = yf.Ticker(ticker)
                price = stock.fast_info.last_price
                market_col.insert_one({"symbol": ticker, "price": price, "timestamp": time.time()})
                print(f"   [MARKET] {ticker}: ${price:.2f}")
            except:
                print(f"   [MARKET] Price fetch failed for {ticker}")

            # 2. SOURCE A: NEW YORK TIMES (Institutional)
            try:
                nyt_articles = fetch_nyt(ticker, name)
                if nyt_articles:
                    for art in nyt_articles:
                        news_col.update_one({"url": art["url"]}, {"$set": art}, upsert=True)
                    print(f"   [NYT] Saved {len(nyt_articles)} articles for {ticker}")
            except Exception as e:
                print(f"   [NYT] Error: {e}")

            # 3. SOURCE B: NEWS API (Global Chatter)
            try:
                api_articles = fetch_newsapi(ticker, name)
                if api_articles:
                    for art in api_articles:
                        news_col.update_one({"url": art["url"]}, {"$set": art}, upsert=True)
                    print(f"   [NEWSAPI] Saved {len(api_articles)} articles for {ticker}")
            except Exception as e:
                print(f"   [NEWSAPI] Error: {e}")
                
            time.sleep(5)

        print("Cycle complete. Sleeping for 2 minutes...")
        time.sleep(120)

if __name__ == "__main__":
    time.sleep(5)
    run_pipeline()