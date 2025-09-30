import tweepy
from config import Config
from loguru import logger

def parse_tweet(tweet):
    """
    Parses a single tweet object to extract relevant information.

    Args:
        tweet (tweepy.Tweet): The tweet object from the Twitter API.

    Returns:
        dict: A dictionary containing the parsed tweet data, or None if parsing fails.
    """
    try:
        content = tweet.text
        username = tweet.author_id  # For v2, you may need to fetch user info separately
        timestamp = tweet.created_at
        engagement = tweet.public_metrics if hasattr(tweet, "public_metrics") else {}
        # Extract mentions and hashtags from content
        mentions = [word for word in content.split() if word.startswith("@")]
        hashtags = [word for word in content.split() if word.startswith("#")]
        return {
            "username": username,
            "timestamp": timestamp,
            "content": content,
            "engagement": engagement,
            "mentions": mentions,
            "hashtags": hashtags,
        }
    except Exception as e:
        logger.error(f"Failed to parse tweet: {e}")
        return None

def scrape_tweets(hashtag, max_tweets=500):
    """
    Scrapes recent tweets for a given hashtag.

    Args:
        hashtag (str): The hashtag to search for.
        max_tweets (int): The maximum number of tweets to scrape.

    Returns:
        list: A list of parsed tweet dictionaries.
    """
    client = tweepy.Client(bearer_token=Config.BEARER_TOKEN, wait_on_rate_limit=True)
    query = f"{hashtag} lang:en -is:retweet"
    tweets = []
    try:
        for tweet in tweepy.Paginator(
            client.search_recent_tweets,
            query=query,
            tweet_fields=["created_at", "author_id", "public_metrics"],
            max_results=100,
        ).flatten(limit=max_tweets):
            parsed = parse_tweet(tweet)
            if parsed:
                tweets.append(parsed)
    except Exception as e:
        logger.error(f"Error fetching tweets for {hashtag}: {e}")
    return tweets

def scrape_all_hashtags(hashtags, max_tweets=500):
    """
    Scrapes tweets for a list of hashtags.

    Args:
        hashtags (list): A list of hashtags to scrape.
        max_tweets (int): The maximum number of tweets to scrape per hashtag.

    Returns:
        list: A list of all parsed tweet dictionaries.
    """
    all_tweets = []
    for tag in hashtags:
        logger.info(f"Scraping tweets for {tag}")
        tweets = scrape_tweets(tag, max_tweets=max_tweets)
        logger.info(f"Collected {len(tweets)} tweets for {tag}")
        all_tweets.extend(tweets)
    return all_tweets

if __name__ == "__main__":
    all_tweets = scrape_all_hashtags(Config.HASHTAGS, max_tweets=Config.MAX_TWEETS_PER_HASHTAG)
    logger.info(f"Total tweets collected: {len(all_tweets)}")