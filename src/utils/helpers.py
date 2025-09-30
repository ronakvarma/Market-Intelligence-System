def log_message(message, level="INFO"):
    import logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger()
    
    if level == "INFO":
        logger.info(message)
    elif level == "WARNING":
        logger.warning(message)
    elif level == "ERROR":
        logger.error(message)
    elif level == "DEBUG":
        logger.debug(message)

def handle_error(error):
    log_message(f"Error occurred: {error}", level="ERROR")

def validate_tweet_data(tweet):
    required_keys = ['id', 'text', 'created_at', 'user']
    return all(key in tweet for key in required_keys)