from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from summarise import legal_text_summarizer, short_summary, medium_summary, long_summary
from language import translate_text
from chatbot import  chatbot_response
from ocr_code import ocr
import os
import traceback
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/page1')
def start():
    return render_template('page1.html')

@app.route('/chatbot')
def start2():
    return render_template('chatbot.html')

@app.route('/api/chatbot', methods=['POST'])
def handle_chat():
    try:
        if not request.is_json:
            return jsonify({'reply': 'Request must be JSON.'}), 400

        user_input = request.json.get('message')
        if not user_input:
            return jsonify({'reply': 'No message provided.'}), 400

        response = chatbot_response(user_input)
        return jsonify({'reply': response})
    except Exception as e:
        traceback.print_exc()
        return jsonify({'reply': 'An error occurred processing your message.'}), 500


@app.route('/process-input', methods=['POST'])
def process_input():
    try:
        text = ""
        summary_length = request.form['summary_length']
        language = request.form['language']

        # Checking if a valid file is uploaded
        file = request.files.get('file', None)
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            text = ocr(file_path) 
        elif 'inputText' in request.form and request.form['inputText'].strip():
            text = request.form['inputText'].strip()

        #based on the summary length chosen
        if summary_length == 'small':
            summary = legal_text_summarizer(text, 400, 600)  
        elif summary_length == 'medium':
            summary = medium_summary(text)  
        elif summary_length == 'large':
            summary = long_summary(text)  
        else:
            summary = 'Invalid summary length specified'

        if language and language != 'en':
            summary = translate_text(summary, language) 
        # print("Summary: ", summary) #debugging
        return render_template('page1.html', summary=summary)

    except Exception as e:
        traceback.print_exc()
        return render_template('page1.html', error='An error occurred while processing the input.')

if __name__ == '__main__':
    app.run(debug=True)


