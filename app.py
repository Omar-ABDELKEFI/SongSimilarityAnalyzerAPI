from app import create_app
import nltk
nltk.data.path.append('/workspace/SongSimilarityAnalyzerAPI/nltk')

app = create_app()


if __name__ == "__main__":
    
    app.run(debug=True)