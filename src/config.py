# Configuration settings for the market intelligence application

class Config:
    # Scraping parameters
    BEARER_TOKEN = "bearer_token"  # Replace with your actual bearer token
    HASHTAGS = ["#nifty50", "#sensex", "#intraday", "#banknifty"]
    MAX_TWEETS_PER_HASHTAG = 200  # Number of tweets to scrape per hashtag
    CHUNK_SIZE = 500  # For chunked processing

    # Data storage paths
    RAW_DATA_PATH = 'data/tweets.json'
    PROCESSED_DATA_PATH = 'data/processed_tweets.parquet'

    # Analysis settings
    SIGNAL_THRESHOLD = 0.5  # Threshold for generating trading signals
    AGGREGATION_WINDOW = 60  # Time window for aggregating signals (in minutes)
    MAX_TFIDF_FEATURES = 100  # Max features for TF-IDF vectorizer

    # Logging
    LOG_FILE = 'logs/market_intel.log'