# Market Intelligence Application - Technical Documentation

## 1. Introduction

This document provides a technical overview of the Market Intelligence Application, a data collection and analysis system focused on real-time market intelligence, specifically targeting discussions around the stock market on Twitter. The application scrapes tweets, processes the data, and performs analysis to generate insights that can aid in trading decisions.

## 2. Architecture

The application follows a modular architecture, with distinct components for scraping, data processing, and analysis. The main components are:

*   **Twitter Scraper:** Collects tweets from Twitter based on specified hashtags.
*   **Data Processor:** Cleans, normalizes, and deduplicates the collected tweet data.
*   **Tweet Analyzer:** Converts tweet content into numerical signals and aggregates them for trading insights.

## 3. Key Modules

### 3.1. `src/twitter_scraper/scraper.py`

This module is responsible for scraping tweets from Twitter. It uses the `tweepy` library to interact with the Twitter API.

*   **`scrape_tweets(hashtag, max_tweets=500)`:** Scrapes recent tweets for a given hashtag.
    *   `hashtag`: The hashtag to search for.
    *   `max_tweets`: The maximum number of tweets to scrape.
*   **`scrape_all_hashtags(hashtags, max_tweets=500)`:** Scrapes tweets for a list of hashtags.
    *   `hashtags`: A list of hashtags to scrape.
    *   `max_tweets`: The maximum number of tweets to scrape per hashtag.
*   **`parse_tweet(tweet)`:** Parses a single tweet object to extract relevant information (username, timestamp, content, engagement, mentions, hashtags).

### 3.2. `src/data_processing/processor.py`

This module is responsible for processing the raw tweet data. It performs the following steps:

*   **Cleaning:** Removes URLs and normalizes Unicode.
*   **Normalization:** Converts usernames and hashtags to lowercase.
*   **Deduplication:** Removes duplicate tweets based on username, timestamp, and content.

The module includes the following functions:

*   **`clean_data(tweets)`:** Cleans the content of tweets.
*   **`normalize_data(tweets)`:** Normalizes usernames and hashtags.
*   **`deduplicate_data(tweets)`:** Deduplicates a list of tweets.
*   **`to_parquet(tweets, filepath)`:** Saves a list of tweets to a Parquet file.
*   **`process_in_chunks(tweets, chunk_size=500)`:** Processes a large list of tweets in smaller, memory-efficient chunks.

### 3.3. `src/analysis/analyzer.py`

This module is responsible for analyzing the processed tweet data. It uses TF-IDF vectorization to convert tweet text into numerical signals.

*   **`TweetAnalyzer(max_features=100)`:** Initializes the TweetAnalyzer with a TF-IDF vectorizer.
    *   `max_features`: The maximum number of features for the TF-IDF vectorizer.
*   **`fit_vectorizer(tweet_texts)`:** Fits the TF-IDF vectorizer on a list of tweet contents.
*   **`text_to_signal(tweet_texts)`:** Transforms a list of tweet texts into a TF-IDF matrix.
*   **`aggregate_signals(tfidf_matrix)`:** Aggregates the TF-IDF signals to produce a single signal vector and a confidence interval.
*   **`plot_signals(signals, sample_size=200)`:** Plots the aggregated signals.

## 4. Data Flow

The data flow within the application is as follows:

1.  The `src/main.py` script starts the application.
2.  The `scrape_all_hashtags` function in `src/twitter_scraper/scraper.py` scrapes tweets from Twitter based on the configured hashtags in `src/config.py`.
3.  The `process_in_chunks` function in `src/data_processing/processor.py` processes the raw tweet data in chunks.
4.  The `TweetAnalyzer` class in `src/analysis/analyzer.py` analyzes the processed tweet data.
5.  The `aggregate_signals` function aggregates the TF-IDF signals to produce a single signal vector and a confidence interval.
6.  The `plot_signals` function plots the aggregated signals.

## 5. Configuration

The application is configured using the `src/config.py` file. This file contains settings such as:

*   `BEARER_TOKEN`: The Twitter API bearer token.
*   `HASHTAGS`: A list of hashtags to scrape.
*   `MAX_TWEETS_PER_HASHTAG`: The maximum number of tweets to scrape per hashtag.
*   `RAW_DATA_PATH`: The path to the raw tweet data file.
*   `PROCESSED_DATA_PATH`: The path to the processed tweet data file.
*   `SIGNAL_THRESHOLD`: The threshold for generating trading signals.
*   `AGGREGATION_WINDOW`: The time window for aggregating signals (in minutes).
*   `MAX_TFIDF_FEATURES`: The maximum number of features for the TF-IDF vectorizer.
*   `LOG_FILE`: The path to the log file.

## 6. Logging

The application uses the `loguru` library for logging. Log messages are written to the `logs/market_intel.log` file. The log file is rotated every 10 MB and compressed using zip.
