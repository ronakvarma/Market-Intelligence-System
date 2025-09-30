import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from loguru import logger

class TweetAnalyzer:
    def __init__(self, max_features=100):
        """
        Initializes the TweetAnalyzer with a TF-IDF vectorizer.

        Args:
            max_features (int): The maximum number of features for the TF-IDF vectorizer.
        """
        self.vectorizer = TfidfVectorizer(max_features=max_features, stop_words='english')
        self.fitted = False

    def fit_vectorizer(self, tweet_texts):
        """
        Fit the TF-IDF vectorizer on a list of tweet contents.
        """
        self.vectorizer.fit(tweet_texts)
        self.fitted = True

    def text_to_signal(self, tweet_texts):
        """
        Transforms a list of tweet texts into a TF-IDF matrix.

        Args:
            tweet_texts (list): A list of tweet content strings.

        Returns:
            numpy.ndarray: The resulting TF-IDF matrix, or None if the vectorizer is not fitted.
        """
        if not self.fitted:
            logger.error("Vectorizer not fitted. Call fit_vectorizer() first.")
            return None
        tfidf_matrix = self.vectorizer.transform(tweet_texts)
        return tfidf_matrix.toarray()

    def aggregate_signals(self, tfidf_matrix):
        """
        Aggregates the TF-IDF signals to produce a single signal vector and a confidence interval.

        Args:
            tfidf_matrix (numpy.ndarray): The TF-IDF matrix.

        Returns:
            tuple: A tuple containing the aggregated signal and the confidence interval, or (None, None) if the input is invalid.
        """
        if tfidf_matrix is None or len(tfidf_matrix) == 0:
            return None, None
        signal = np.mean(tfidf_matrix, axis=1)
        mean_signal = np.mean(signal)
        std_signal = np.std(signal)
        conf_interval = (mean_signal - 1.96 * std_signal, mean_signal + 1.96 * std_signal)
        return signal, conf_interval

    def plot_signals(self, signals, sample_size=200):
        """
        Plots the aggregated signals, using sampling for memory efficiency if the dataset is large.

        Args:
            signals (numpy.ndarray): The aggregated signal vector.
            sample_size (int): The number of data points to sample for plotting.
        """
        if len(signals) > sample_size:
            idx = np.random.choice(len(signals), sample_size, replace=False)
            signals = np.array(signals)[idx]
        plt.figure(figsize=(10, 4))
        plt.plot(signals, marker='o', linestyle='-', alpha=0.7)
        plt.title("Sampled Tweet Signal Strengths")
        plt.xlabel("Sample Index")
        plt.ylabel("Signal Value")
        plt.tight_layout()
        plt.show()