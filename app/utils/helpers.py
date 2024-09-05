import numpy as np

def safe_mean(values):
    """Calculate mean safely, handling potential type mismatches."""
    valid_values = [v for v in values if isinstance(v, (int, float)) and not np.isnan(v)]
    return sum(valid_values) / len(valid_values) if valid_values else 0

def calculate_similarity(song1, song2):
    similarities = []

    # Tempo similarity
    if 'tempo' in song1['audio'] and 'tempo' in song2['audio']:
        tempo_sim = 1 - abs(song1['audio']['tempo'] - song2['audio']['tempo']) / max(song1['audio']['tempo'], song2['audio']['tempo'])
        similarities.append(tempo_sim)

    # MFCC similarity
    if 'mfccs' in song1['audio'] and 'mfccs' in song2['audio']:
        min_mfcc_length = min(len(song1['audio']['mfccs']), len(song2['audio']['mfccs']))
        if min_mfcc_length > 0:
            mfcc_corr = np.corrcoef(song1['audio']['mfccs'][:min_mfcc_length], song2['audio']['mfccs'][:min_mfcc_length])[0, 1]
            similarities.append(mfcc_corr)

    # Chroma similarity
    if 'chroma' in song1['audio'] and 'chroma' in song2['audio']:
        min_chroma_length = min(len(song1['audio']['chroma']), len(song2['audio']['chroma']))
        if min_chroma_length > 0:
            chroma_corr = np.corrcoef(song1['audio']['chroma'][:min_chroma_length], song2['audio']['chroma'][:min_chroma_length])[0, 1]
            similarities.append(chroma_corr)

    # Audio similarity is the average of available similarities
    audio_similarity = safe_mean(similarities)

    # Lyric similarity
    lyric_similarities = []

    # Sentiment similarity
    if 'sentiment' in song1['lyrics'] and 'sentiment' in song2['lyrics']:
        sentiment_sim = song1['lyrics']['sentiment']['compound'] * song2['lyrics']['sentiment']['compound']
        lyric_similarities.append(sentiment_sim)

    # Topic similarity
    if song1['lyrics'].get('topics') and song2['lyrics'].get('topics'):
        topic_sim = len(set(song1['lyrics']['topics'][0]).intersection(set(song2['lyrics']['topics'][0]))) / 10
        lyric_similarities.append(topic_sim)

    # Vocabulary complexity similarity
    if 'vocabulary_complexity' in song1['lyrics'] and 'vocabulary_complexity' in song2['lyrics']:
        vocab_sim = 1 - abs(song1['lyrics']['vocabulary_complexity'] - song2['lyrics']['vocabulary_complexity'])
        lyric_similarities.append(vocab_sim)

    # Lyric similarity is the average of available similarities
    lyric_similarity = safe_mean(lyric_similarities)

    # Overall similarity is the average of audio and lyric similarities
    return safe_mean([audio_similarity, lyric_similarity])