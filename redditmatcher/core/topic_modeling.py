import os
import ssl
import nltk
import re
from bertopic import BERTopic

import os
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer

# SSL fix for some environments
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Download stopwords if not already downloaded
nltk.download('stopwords')
STOP_WORDS = set(stopwords.words('english'))

def preprocess_text(text):
    """Clean and preprocess input text."""
    text = text.lower()
    text = re.sub(r'\b\w{1,2}\b', '', text)           # Remove short words
    text = re.sub(r'http\S+', '', text)               # Remove URLs
    tokens = [word for word in re.findall(r'\b\w+\b', text) if word not in STOP_WORDS]
    return ' '.join(tokens)

def trim_topic_label(label, max_words=3):
    """Trim topic label to at most max_words words."""
    label = re.sub(r'[^\w\s]', '', label)
    words = label.strip().split()
    return " ".join(words[:max_words])

def get_topic_distribution(texts, use_keybert=False):
    """
    Fit BERTopic on the given texts for concise topic labels.
    Args:
        texts (list of dict): each dict with 'body' (string)
        use_keybert (bool): if True, use KeyBERTInspired for topic names; else use LLM
    Returns:
        topic_info (DataFrame): Info about topics (labels, document counts, etc.)
        topic_distr (DataFrame): Mapping of docs to topics
    """
    if not texts:
        return None, None

    preprocessed_docs = []
    for d in texts:
        if d.get("body") and isinstance(d["body"], str) and len(d["body"]) > 15:
            processed_text = preprocess_text(str(d.get("body", "")))
            if processed_text.strip():  # Only add if not empty or just whitespace
                preprocessed_docs.append(processed_text)
    
    if not preprocessed_docs:
        return None, None

    # Choose representation model
    representation_model = None # Will be set later if needed

    # Initialize Gemini model for topic naming
    import google.generativeai as genai
    import json
    from dotenv import load_dotenv

    load_dotenv()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
        gemini_model = genai.GenerativeModel("gemini-1.5-flash")

    vectorizer_model = CountVectorizer(
        max_features=3000,
        stop_words="english",
        ngram_range=(1,2)
    )

    topic_model = BERTopic(
        min_topic_size=5,
        verbose=False,
        vectorizer_model=vectorizer_model
    )

    topics, _ = topic_model.fit_transform(preprocessed_docs)
    topic_info = topic_model.get_topic_info()

    # Generate topic names using Gemini
    new_topic_names = {}
    for index, row in topic_info.iterrows():
        topic_id = row['Topic']
        if topic_id == -1: # -1 is for outliers, keep as default
            new_topic_names[topic_id] = "Outlier Topic"
            continue

        keywords = ", ".join([word[0] for word in topic_model.get_topic(topic_id)])
        prompt = f"""Analyze the following keywords and generate a concise, descriptive topic name of 2-3 words. 
        Example: 
        Keywords: game, release, update, community
        Topic Name: Gaming News & Community

        Keywords: {keywords}
        Topic Name:"""
        
        try:
            response = gemini_model.generate_content(prompt)
            generated_name = response.text.strip()
            new_topic_names[topic_id] = trim_topic_label(generated_name, max_words=3)
        except Exception as e:
            print(f"Error generating name for topic {topic_id}: {e}")
            new_topic_names[topic_id] = f"Topic {topic_id}"

    # Update topic names in topic_info
    topic_info['Name'] = topic_info['Topic'].map(new_topic_names)

    topic_distr = topic_model.get_document_info(preprocessed_docs)
    return topic_info, topic_distr
        