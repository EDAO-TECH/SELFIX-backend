from flask import Flask, request, jsonify
import logging
import os

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Root route
@app.route('/')
def index():
    logger.info("Root route accessed")
    return jsonify({"message": "SELFIX GPT API is running"})

# Health check
@app.route('/api/ping', methods=['GET'])
def ping():
    logger.info("Ping received")
    return jsonify({"message": "GPT API is up"})

# Simulated response generator
@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.get_json()
    prompt = data.get("prompt", "")
    logger.info(f"Prompt received: {prompt}")
    response = f"[Simulated response] You said: {prompt}"
    return jsonify({
        "prompt": prompt,
        "response": response
    })

# Karma score endpoint
@app.route('/api/karma-score', methods=['GET'])
def karma_score():
    logger.info("Karma score requested")
    return jsonify({"karma": 42})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8825))
    app.run(host='0.0.0.0', port=port, debug=True)
