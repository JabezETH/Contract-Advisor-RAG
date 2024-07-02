from flask import Flask, request, jsonify
import sys
import logging
import os
from flask_cors import CORS

sys.path.insert(1, '/home/jabez/week_11/Contract-Advisor-RAG/scripts')
import data_processing
import pipeline

app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "*"}})

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Set watchdog logging to WARNING to reduce verbosity
logging.getLogger('watchdog').setLevel(logging.WARNING)

@app.route('/chat', methods=['POST'])
def execute():
    try:
        data = request.json
        logging.debug(f"Request received: {data}")
        
        if not data or 'message' not in data:
            raise ValueError("Invalid input data")
        
        user_input = data.get('message')
        logging.debug(f"User input: {user_input}")
        
        file_path = os.getenv('FILE_PATH', '/home/jabez/week_11/Contract-Advisor-RAG/data/Raptor Contract.docx')
        logging.debug(f"File path: {file_path}")
        
        # Load and process the document
        doc = data_processing.doc_loader(file_path)
        logging.debug("Document loaded successfully")
        
        vector = data_processing.text_splitter(doc)
        logging.debug("Document processed into vectors")
        
        # Generate the chatbot response
        result = pipeline.chatbot(vector, user_input)
        logging.debug(f"Chatbot response: {result}")
        
        return jsonify({'response': result})
    except ValueError as ve:
        logging.error(f"ValueError: {ve}", exc_info=True)
        return jsonify({'output': f"ValueError: {str(ve)}"}), 400
    except FileNotFoundError as fnf:
        logging.error(f"FileNotFoundError: {fnf}", exc_info=True)
        return jsonify({'output': f"FileNotFoundError: {str(fnf)}"}), 404
    except Exception as e:
        logging.error(f"Error processing request: {e}", exc_info=True)
        return jsonify({'output': f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
