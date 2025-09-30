import os
from loguru import logger
from config import Config
from twitter_scraper.scraper import scrape_all_hashtags
from data_processing.processor import DataProcessor
from analysis.analyzer import TweetAnalyzer

def main():
    """
    Main function to orchestrate the scraping, processing, and analysis of tweets.

    The workflow is as follows:
    1.  Set up logging and ensure necessary directories exist.
    2.  Scrape tweets from Twitter based on the configured hashtags.
    3.  Process the raw tweets in chunks to clean, normalize, and deduplicate them.
    4.  Save the processed tweets to a Parquet file.
    5.  Analyze the tweet content using a TF-IDF vectorizer to generate signals.
    6.  Aggregate the signals and plot them for visualization.
    """
    # Ensure data and logs directories exist
    os.makedirs(os.path.dirname(Config.RAW_DATA_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(Config.LOG_FILE), exist_ok=True)

    # Configure logging
    logger.add(Config.LOG_FILE, rotation="10 MB", compression="zip", level="INFO")
    logger.info("Starting the market intelligence application.")

    # 1. Scrape tweets
    logger.info("Scraping tweets...")
    raw_tweets = scrape_all_hashtags(Config.HASHTAGS, max_tweets=Config.MAX_TWEETS_PER_HASHTAG)
    if not raw_tweets:
        logger.warning("No tweets were scraped. Exiting.")
        return

    # 2. Process tweets
    logger.info("Processing tweets...")
    processor = DataProcessor()
    processed_tweets = []
    for chunk in processor.process_in_chunks(raw_tweets, chunk_size=Config.CHUNK_SIZE):
        processed_tweets.extend(chunk)
    
    if not processed_tweets:
        logger.warning("No tweets remaining after processing. Exiting.")
        return

    # Save processed data
    processor.to_parquet(processed_tweets, Config.PROCESSED_DATA_PATH)

    # 3. Analyze tweets
    logger.info("Analyzing tweets...")
    analyzer = TweetAnalyzer(max_features=Config.MAX_TFIDF_FEATURES)
    
    tweet_texts = [tweet['content'] for tweet in processed_tweets]
    analyzer.fit_vectorizer(tweet_texts)
    
    tfidf_matrix = analyzer.text_to_signal(tweet_texts)
    
    if tfidf_matrix is not None:
        signals, conf_interval = analyzer.aggregate_signals(tfidf_matrix)
        if signals is not None:
            logger.info(f"Aggregated signal mean: {signals.mean():.4f}")
            logger.info(f"Confidence Interval: {conf_interval}")
            analyzer.plot_signals(signals)
    
    logger.info("Market intelligence application finished.")

if __name__ == "__main__":
    main()