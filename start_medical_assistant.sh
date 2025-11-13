#!/bin/bash

echo "🚀 Starting Medical Plan Assistant with Gemini Flash 2.5..."
echo ""
echo "📋 Make sure you have installed the dependencies:"
echo "   pip install -r requirements.txt"
echo ""

# Check if port 5000 is already in use
if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "⚠️  Port 5000 is already in use!"
    echo "   Stopping existing server..."
    kill $(lsof -t -i:5000)
    sleep 2
fi

# Start the server
echo "✅ Starting Flask server..."
python3 app.py

# Alternative: To run in background, uncomment below and comment above
# nohup python3 app.py > server.log 2>&1 &
# echo "✅ Server started in background"
# echo "📝 Check server.log for logs"
# echo ""
# echo "🌐 Open http://localhost:5000 in your browser"
# echo ""
# echo "To stop the server, run:"
# echo "   kill \$(lsof -t -i:5000)"

