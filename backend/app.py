from flask import Flask, request, jsonify
import sys
import logging
import os
from flask_cors import CORS


sys.path.insert(1, '/home/jabez/Documents/week_11/Contract-Advisor-RAG/scripts')
# import data_processing
# import pipeline
import autogen_agent

app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "*"}})

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Set watchdog logging to WARNING to reduce verbosity
logging.getLogger('watchdog').setLevel(logging.WARNING)

@app.route('/chat', methods=['POST'])
def execute():
    try:
        data = request.form
        logging.debug(f"Request received: {data}")

        if not data or 'message' not in data:
            raise ValueError("Invalid input data")

        user_input = data.get('message')
        logging.debug(f"User input: {user_input}")

        file = request.files.get('file')
        if file:
            file_path = os.path.join('/home/jabez/Documents/week_11/Contract-Advisor-RAG/uploaded', file.filename)
            file.save(file_path)
            logging.debug(f"File uploaded to: {file_path}")
        else:
            file_path = os.getenv('FILE_PATH', '/home/jabez/Documents/week_11/Contract-Advisor-RAG/data/document.md')
            logging.debug(f"Default file path: {file_path}")

        # Assuming autogen_bot returns a dictionary with 'content' and 'role'
        result = autogen_agent.autogen_bot(file_path, user_input)
        logging.debug(f"Chatbot response: {result}")

        if not isinstance(result, dict) or 'content' not in result or 'role' not in result:
            raise ValueError("Invalid response format from autogen_bot")

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
