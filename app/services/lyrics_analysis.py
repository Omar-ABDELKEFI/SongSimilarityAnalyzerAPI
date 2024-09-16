import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np


nltk.data.path.append('/app/nltk')


sia = SentimentIntensityAnalyzer()

def analyze_lyrics(lyrics):
    # Tokenize and remove stopwords
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(lyrics.lower())
    filtered_words = [word for word in words if word.isalnum() and word not in stop_words]

    # Sentiment analysis
    sentiment = sia.polarity_scores(lyrics)

    # Topic modeling
    vectorizer = CountVectorizer(max_df=1.0, min_df=1, stop_words='english')
    doc_term_matrix = vectorizer.fit_transform([lyrics])
    n_topics = min(3, len(vectorizer.get_feature_names_out()))

    topics = []
    if n_topics > 0:
        lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
        lda.fit(doc_term_matrix)
        feature_names = vectorizer.get_feature_names_out()
        for topic_idx, topic in enumerate(lda.components_):
            top_words = [feature_names[i] for i in topic.argsort()[:-10 - 1:-1]]
            topics.append(top_words)
    else:
        topics = []

    return {
        'sentiment': sentiment,
        'topics': topics,
        'vocabulary_complexity': len(set(filtered_words)) / len(filtered_words) if filtered_words else 0
    }
