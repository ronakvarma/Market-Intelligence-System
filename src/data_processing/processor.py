import pandas as pd
import unicodedata
from loguru import logger

class DataProcessor:
    def clean_data(self, tweets):
        """
        Cleans the content of tweets by removing URLs, normalizing Unicode, and filtering out empty tweets.

        Args:
            tweets (list): A list of tweet dictionaries.

        Returns:
            list: A list of cleaned tweet dictionaries.
        """
        cleaned_tweets = []
        for tweet in tweets:
            try:
                content = tweet.get("content", "")
                # Remove URLs
                content = ' '.join(word for word in content.split() if not word.startswith('http'))
                # Normalize Unicode
                content = unicodedata.normalize("NFKC", content)
                tweet["content"] = content.strip()
                # Remove empty content
                if content:
                    cleaned_tweets.append(tweet)
            except Exception as e:
                logger.error(f"Error cleaning tweet: {e}")
        return cleaned_tweets

    def normalize_data(self, tweets):
        """
        Normalizes usernames and hashtags to lowercase for consistency.

        Args:
            tweets (list): A list of tweet dictionaries.

        Returns:
            list: A list of normalized tweet dictionaries.
        """
        for tweet in tweets:
            tweet["username"] = tweet.get("username", "").lower()
            tweet["hashtags"] = [h.lower() for h in tweet.get("hashtags", [])]
        return tweets

    def deduplicate_data(self, tweets):
        """
        Deduplicates a list of tweets based on a composite key of username, timestamp, and content.

        Args:
            tweets (list): A list of tweet dictionaries.

        Returns:
            list: A list of unique tweet dictionaries.
        """
        seen = set()
        unique_tweets = []
        for tweet in tweets:
            key = (tweet.get("username"), tweet.get("timestamp"), tweet.get("content"))
            if key not in seen:
                seen.add(key)
                unique_tweets.append(tweet)
        return unique_tweets

    def to_parquet(self, tweets, filepath):
        """
        Saves a list of tweets to a Parquet file with a predefined schema.

        Args:
            tweets (list): A list of tweet dictionaries.
            filepath (str): The path to the output Parquet file.
        """
        if not tweets:
            logger.warning("No tweets to save.")
            return
        df = pd.DataFrame(tweets)
        # Ensure schema columns
        schema = ["username", "timestamp", "content", "engagement", "mentions", "hashtags"]
        for col in schema:
            if col not in df.columns:
                df[col] = None
        df = df[schema]
        df.to_parquet(filepath, index=False)
        logger.info(f"Saved {len(df)} tweets to {filepath}")

    def process_in_chunks(self, tweets, chunk_size=500):
        """
        Processes a large list of tweets in smaller, memory-efficient chunks.

        Args:
            tweets (list): A list of tweet dictionaries.
            chunk_size (int): The number of tweets to process in each chunk.

        Yields:
            list: A chunk of processed tweet dictionaries.
        """
        for i in range(0, len(tweets), chunk_size):
            chunk = tweets[i:i+chunk_size]
            cleaned = self.clean_data(chunk)
            normalized = self.normalize_data(cleaned)
            unique = self.deduplicate_data(normalized)
            yield unique