import nltk
nltk.data.path.append('/workspace/SongSimilarityAnalyzerAPI/nltk')
nltk.download('punkt', download_dir='/workspace/SongSimilarityAnalyzerAPI/nltk')
nltk.download('stopwords', download_dir='/workspace/SongSimilarityAnalyzerAPI/nltk')
nltk.download('vader_lexicon', download_dir='/workspace/SongSimilarityAnalyzerAPI/nltk')
nltk.download('punkt_tab', download_dir='/workspace/SongSimilarityAnalyzerAPI/nltk')
# print(nltk.data.path,"nltk.data.path")