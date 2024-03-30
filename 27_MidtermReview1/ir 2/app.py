from flask import Flask, request, jsonify, render_template
from your_script import summarise_pegasus, preprocess_text
import traceback


app = Flask(__name__)

@app.route('/')
def index():
    # Render the main page
    return render_template('index.html')

@app.route('/process-input', methods=['POST'])
def process_input():
    try:
        # Parse the JSON request and get the text to be processed
        data = request.get_json()
        text = data['text']
        
        # Preprocess and summarize the text
        preprocessed_text = preprocess_text(text)
        summary = summarise_pegasus(preprocessed_text)
        
        # Check if summary is not empty or null
        if summary:
            return jsonify({'output': summary})
        else:
            return jsonify({'output': 'No summary was generated.'})
    except Exception as e:
        # Log the full stack trace and return a detailed error message
        traceback.print_exc()
        return jsonify({'error': 'An error occurred while processing the text.', 'trace': traceback.format_exc()}), 500

if __name__ == '__main__':
    app.run(debug=True)
