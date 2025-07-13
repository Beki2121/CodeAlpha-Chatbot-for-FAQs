# Enhanced FAQ Chatbot

A Python-based FAQ Chatbot with advanced features including voice input/output, semantic matching, and mobile-friendly interface.

## Features

### Core Features
- **Multi-format FAQ Loading**: Supports both JSON and CSV file formats
- **Advanced NLP Processing**: Uses SpaCy for tokenization, lemmatization, and stop word removal
- **Semantic Matching**: Implements Sentence Transformers for better question understanding
- **Smart Answer Highlighting**: Highlights relevant keywords in responses
- **Search Suggestions**: Provides real-time question suggestions as you type

### Enhanced Features
- **Voice Input/Output**: 
  - Speech-to-text for voice questions
  - Text-to-speech for bot responses
- **Mobile-Friendly Design**: Responsive interface that works on all devices
- **Comprehensive Logging**: Tracks user interactions and system performance
- **Confidence Scoring**: Shows matching confidence for transparency

### User Interface
- Modern, gradient-based design
- Real-time typing indicators
- Clickable question suggestions
- Voice recording with visual feedback
- Responsive layout for mobile devices

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Chatbot-for-FAQs
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install SpaCy English model**:
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. **Install additional system dependencies** (for voice features):
   - **Windows**: Install PyAudio: `pip install pyaudio`
   - **macOS**: `brew install portaudio`
   - **Linux**: `sudo apt-get install portaudio19-dev python3-pyaudio`

## Usage

1. **Prepare your FAQ data**:
   - Use `faq_data.json` for JSON format
   - Use `faq_data.csv` for CSV format
   - Both files should have `question` and `answer` columns

2. **Run the application**:
   ```bash
   python app.py
   ```

3. **Access the chatbot**:
   - Open your browser and go to `http://127.0.0.1:5000/`
   - Start asking questions!

## File Structure

```
Chatbot-for-FAQs/
├── app.py                 # Main Flask application
├── faq_data.json         # FAQ data in JSON format
├── faq_data.csv          # FAQ data in CSV format
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── templates/
│   └── chat.html        # Chat interface
└── chatbot.log          # Application logs (created automatically)
```

## API Endpoints

- `GET /` - Main chat interface
- `POST /chat` - Process user questions
- `POST /suggestions` - Get search suggestions
- `POST /voice-input` - Convert speech to text
- `POST /voice-output` - Convert text to speech
- `GET /analytics` - Get basic analytics

## Configuration

### FAQ Data Format

**JSON Format**:
```json
[
  {
    "question": "What is your return policy?",
    "answer": "You can return any item within 30 days of purchase for a full refund."
  }
]
```

**CSV Format**:
```csv
question,answer
"What is your return policy?","You can return any item within 30 days of purchase for a full refund."
```

### Customization

- **Similarity Threshold**: Modify the confidence threshold in `app.py` (default: 0.3)
- **Voice Settings**: Adjust speech recognition and TTS parameters
- **UI Styling**: Customize colors and layout in `templates/chat.html`

## Troubleshooting

### Common Issues

1. **SpaCy Model Not Found**:
   ```bash
   python -m spacy download en_core_web_sm
   ```

2. **Voice Input Not Working**:
   - Check microphone permissions
   - Install PyAudio: `pip install pyaudio`
   - Ensure internet connection for Google Speech Recognition

3. **Sentence Transformers Download**:
   - First run may take time to download the model
   - Ensure stable internet connection

### Logs

Check `chatbot.log` for detailed application logs and error messages.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions, please check the logs or create an issue in the repository. 