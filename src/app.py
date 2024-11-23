from flask import Flask, render_template, request
from llama_index import VectorStoreIndex, ServiceContext, Document
from llama_index.llms import OpenAI
import openai
import pypdf
import os

# Đặt API key
openai.api_key = 'import or insert your open ai api key here'

# Cấu hình thư mục upload
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'upload')

def read_data():
    reader = SimpleDirectoryReader(input_dir=UPLOAD_FOLDER, recursive=True)
    docs = reader.load_data()
    service_context = ServiceContext.from_defaults(
        llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt="You are an expert on the docs and can provide helpful summaries")
    )
    index = VectorStoreIndex.from_documents(docs, service_context=service_context)
    chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)
    return chat_engine

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'pdf_file' in request.files:
        pdf_file = request.files['pdf_file']
        if pdf_file.filename.endswith('.pdf'):
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
            pdf_file.save(pdf_path)
            print(f"Uploaded PDF path: {pdf_path}")
            return render_template('chat.html', upload_success=True)
        else:
            return render_template('index.html', upload_error="Invalid file format. Please upload a PDF.")
    else:
        return render_template('index.html', upload_error="No file uploaded.")

@app.route('/chat', methods=['POST'])
def chat():
    chat_engine = read_data()
    if request.method == 'POST':
        prompt = request.form['prompt']
        response = chat_engine.chat(prompt)
        return render_template('chat.html', prompt=prompt, response=response.response)

if __name__ == '__main__':
    app.run(debug=True)
