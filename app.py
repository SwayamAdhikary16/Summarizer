from flask import Flask, render_template, request, jsonify
from utils import extract_text_from_pdf, summarize_text_with_gemini
import os
import tempfile
import PyPDF2

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

from flask import Flask, render_template, request
from utils import extract_text_from_pdf, summarize_text_with_gemini
import os
import tempfile
import PyPDF2

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    pdf_url = request.form.get('pdf_url')
    if pdf_url:
        text = extract_text_from_pdf(pdf_url)
    else:
        uploaded_file = request.files.get('pdf_file')
        if uploaded_file and uploaded_file.filename.endswith('.pdf'):
            temp_path = os.path.join(tempfile.gettempdir(), uploaded_file.filename)
            uploaded_file.save(temp_path)
            with open(temp_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in range(len(reader.pages)):
                    text += reader.pages[page].extract_text()
        else:
            return "Please provide a valid PDF file."

    if text:
        summary = summarize_text_with_gemini(text)
        print("Summary generated")
        return render_template('summary.html', summary=summary)
    
    else:
        return "Failed to extract text from the provided PDF."

if __name__ == '__main__':
    app.run(debug=True)