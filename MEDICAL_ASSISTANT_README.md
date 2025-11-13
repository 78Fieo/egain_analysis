# Medical Plan Assistant with Gemini Flash 2.5

An AI-powered medical insurance assistant that helps users select the best medical plan for their needs using Google's Gemini Flash 2.5 API.

## Features

- 🤖 **AI Chat Assistant**: Powered by Gemini Flash 2.5 for intelligent conversations
- 💬 **Real-time Chat**: Instant responses with typing indicators
- 📋 **Plan Comparison**: Side-by-side comparison of multiple medical plans
- 🎯 **Personalized Recommendations**: AI suggests the best plan based on user profile
- 💡 **Interactive Interface**: Click on plans to ask questions about them
- 🔄 **Conversation Memory**: Maintains context throughout the session

## Installation

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Start the Flask server**:
```bash
python app.py
```

3. **Open your browser**:
Navigate to `http://localhost:5000`

## How It Works

### Backend (app.py)
- Flask server with CORS enabled
- Gemini Flash 2.5 API integration
- Session-based conversation history
- RESTful API endpoints for chat

### Frontend (medical_assistant.html)
- Clean, modern UI inspired by Apple design
- Real-time chat interface
- Medical plan cards with hover effects
- Responsive design for mobile and desktop

## API Endpoints

### POST /api/chat
Send a message to the AI assistant.

**Request Body**:
```json
{
  "message": "What's the difference between HMO and PPO?",
  "session_id": "session_12345"
}
```

**Response**:
```json
{
  "response": "HMO (Health Maintenance Organization) requires...",
  "session_id": "session_12345"
}
```

### POST /api/reset
Reset the conversation history for a session.

**Request Body**:
```json
{
  "session_id": "session_12345"
}
```

## Customization

### Adding More Plans
Edit the `medical_assistant.html` file and add more plan cards in the `.plans-grid` section:

```html
<div class="plan-card">
    <div class="plan-name">Your Plan Name</div>
    <div class="plan-type">Plan Type</div>
    <div class="plan-price">$XXX</div>
    <div class="plan-price-label">per month</div>
    <ul class="plan-features">
        <li>Feature 1</li>
        <li>Feature 2</li>
    </ul>
</div>
```

### Changing the AI Model
To use a different Gemini model, edit `app.py`:

```python
model = genai.GenerativeModel('gemini-pro')  # or another model
```

### Customizing the System Prompt
Modify the system prompt in `app.py` to change how the AI assistant behaves:

```python
system_prompt = """Your custom instructions here..."""
```

## Security Notes

⚠️ **Important**: The API key is currently hardcoded in `app.py`. For production:

1. Use environment variables:
```python
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
```

2. Create a `.env` file:
```
GEMINI_API_KEY=your_key_here
```

3. Use python-dotenv to load it:
```python
from dotenv import load_dotenv
load_dotenv()
```

## Troubleshooting

### "Module not found" errors
Make sure you've installed all requirements:
```bash
pip install -r requirements.txt
```

### CORS errors
The Flask-CORS library should handle this, but if you encounter issues, check that CORS is properly configured in `app.py`.

### API Connection errors
- Ensure your Gemini API key is valid
- Check your internet connection
- Verify the Flask server is running on port 5000

## Future Enhancements

- [ ] Add user profile form to collect family size, usage, etc.
- [ ] Implement plan selection and checkout flow
- [ ] Add cost calculator
- [ ] Save conversation history to database
- [ ] Add authentication
- [ ] Deploy to production server

## Tech Stack

- **Backend**: Flask (Python)
- **AI**: Google Gemini Flash 2.5
- **Frontend**: HTML, CSS, Vanilla JavaScript
- **Styling**: Custom CSS (Apple-inspired design)

## License

MIT License - Feel free to use and modify as needed.

