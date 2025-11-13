from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__, static_folder='.')
CORS(app)

# Configure Gemini API
GEMINI_API_KEY = "AIzaSyBeaGTa3_LAcG3ZnWpdqsi-vItXzGtIAn8"
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the model
model = genai.GenerativeModel('gemini-2.0-flash-exp')

# Store conversation history per session
conversations = {}

@app.route('/')
def index():
    return send_from_directory('.', 'medical_assistant.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        session_id = data.get('session_id', 'default')
        
        # Get or create conversation history for this session
        if session_id not in conversations:
            conversations[session_id] = model.start_chat(history=[])
            # Set the system context
            system_prompt = """You are a helpful medical insurance assistant. You help users:
            - Choose the right medical plan based on their needs
            - Understand different plan types (HMO, PPO, etc.)
            - Compare costs, coverage, and benefits
            - Answer questions about medical insurance
            
            Be friendly, concise, and informative. When recommending plans, consider:
            - Family size
            - Healthcare usage (low, moderate, high)
            - Budget constraints
            - Preferred providers
            
            Current context: User is on Step 1 of 5 - Medical Plan Selection"""
            
            conversations[session_id].send_message(system_prompt)
        
        chat = conversations[session_id]
        
        # Send user message and get response
        response = chat.send_message(user_message)
        
        return jsonify({
            'response': response.text,
            'session_id': session_id
        })
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            'error': str(e),
            'response': "I apologize, but I encountered an error. Please try again."
        }), 500

@app.route('/api/reset', methods=['POST'])
def reset_conversation():
    try:
        data = request.json
        session_id = data.get('session_id', 'default')
        
        if session_id in conversations:
            del conversations[session_id]
        
        return jsonify({'status': 'success', 'message': 'Conversation reset'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting Medical Assistant with Gemini Flash 2.5...")
    print("Open http://localhost:5000 in your browser")
    app.run(debug=True, port=5000, host='0.0.0.0')

