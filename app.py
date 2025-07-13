import json
import csv
import logging
import re
from datetime import datetime
from flask import Flask, render_template, request, jsonify
import spacy
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import speech_recognition as sr
from gtts import gTTS
import os
import io
import base64

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chatbot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load SpaCy English model
nlp = spacy.load('en_core_web_sm')

# Load Sentence Transformer for better semantic matching
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load FAQ data (supports both JSON and CSV)
def load_faqs():
    faqs = []
    # Try JSON first
    try:
        with open('faq_data.json', 'r', encoding='utf-8') as f:
            faqs = json.load(f)
            logger.info(f"Loaded {len(faqs)} FAQs from JSON file")
    except FileNotFoundError:
        # Try CSV if JSON not found
        try:
            with open('faq_data.csv', 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                faqs = list(reader)
                logger.info(f"Loaded {len(faqs)} FAQs from CSV file")
        except FileNotFoundError:
            logger.error("No FAQ data file found (faq_data.json or faq_data.csv)")
            return []
    return faqs

faqs = load_faqs()
questions = [faq['question'] for faq in faqs]
answers = [faq['answer'] for faq in faqs]

def preprocess(text):
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return ' '.join(tokens)

# Create embeddings for all FAQ questions
question_embeddings = model.encode(questions)

def highlight_keywords(answer, user_question):
    """Highlight keywords in the answer that match the user's question"""
    user_words = set(preprocess(user_question).split())
    answer_words = answer.split()
    highlighted_words = []
    
    for word in answer_words:
        clean_word = re.sub(r'[^\w\s]', '', word.lower())
        if clean_word in user_words and len(clean_word) > 2:
            highlighted_words.append(f'<mark>{word}</mark>')
        else:
            highlighted_words.append(word)
    
    return ' '.join(highlighted_words)

def get_search_suggestions(query, limit=5):
    """Get search suggestions based on partial user input"""
    if len(query) < 2:
        return []
    
    suggestions = []
    query_lower = query.lower()
    
    for question in questions:
        if query_lower in question.lower():
            suggestions.append(question)
            if len(suggestions) >= limit:
                break
    
    return suggestions

def make_links_clickable(text):
    import re
    url_pattern = re.compile(r'(https?://[\w\.-/\?&=%#]+)')
    return url_pattern.sub(r'<a href="\1" target="_blank" rel="noopener noreferrer">\1</a>', text)

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '')
    
    # Log user question
    logger.info(f"User question: {user_input}")
    
    # Get search suggestions
    suggestions = get_search_suggestions(user_input)
    
    # Encode user input
    user_embedding = model.encode([user_input])
    
    # Calculate similarities
    similarities = cosine_similarity(user_embedding, question_embeddings).flatten()
    best_idx = np.argmax(similarities)
    best_similarity = similarities[best_idx]
    
    # Log matching info
    logger.info(f"Best match: {questions[best_idx]} (similarity: {best_similarity:.3f})")
    
    if best_similarity < 0.3:
        response = "Sorry, I don't have an answer for that. Could you please rephrase your question?"
        logger.info("No good match found")
    else:
        answer = answers[best_idx]
        # Highlight keywords in the answer
        highlighted_answer = highlight_keywords(answer, user_input)
        # Make links clickable
        highlighted_answer = make_links_clickable(highlighted_answer)
        response = highlighted_answer
        logger.info(f"Answered with: {answer}")
    
    return jsonify({
        'answer': response,
        'suggestions': suggestions,
        'confidence': float(best_similarity)
    })

@app.route('/suggestions', methods=['POST'])
def get_suggestions():
    query = request.json.get('query', '')
    suggestions = get_search_suggestions(query)
    return jsonify({'suggestions': suggestions})

@app.route('/voice-input', methods=['POST'])
def voice_input():
    """Handle voice input and convert to text"""
    try:
        audio_data = request.files['audio']
        recognizer = sr.Recognizer()
        
        with sr.AudioFile(audio_data) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            
        logger.info(f"Voice input converted: {text}")
        return jsonify({'text': text, 'success': True})
    except Exception as e:
        logger.error(f"Voice input error: {str(e)}")
        return jsonify({'error': 'Could not process voice input', 'success': False})

@app.route('/voice-output', methods=['POST'])
def voice_output():
    """Convert text to speech"""
    try:
        text = request.json.get('text', '')
        tts = gTTS(text=text, lang='en')
        
        # Save to bytes buffer
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        # Convert to base64 for sending to frontend
        audio_base64 = base64.b64encode(audio_buffer.read()).decode()
        
        return jsonify({
            'audio': audio_base64,
            'success': True
        })
    except Exception as e:
        logger.error(f"Voice output error: {str(e)}")
        return jsonify({'error': 'Could not generate speech', 'success': False})

@app.route('/analytics')
def analytics():
    """Get analytics data"""
    # This would typically come from a database
    # For now, return basic stats
    return jsonify({
        'total_faqs': len(faqs),
        'categories': ['General', 'Shipping', 'Returns', 'Support'],
        'popular_questions': questions[:5]
    })

if __name__ == '__main__':
    app.run(debug=True) 