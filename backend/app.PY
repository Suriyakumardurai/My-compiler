from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
import tempfile
import os

app = Flask(__name__, static_folder='../my-frontend/build')
CORS(app)

@app.route('/compile', methods=['POST'])
def compile_code():
    code = request.json.get('code')
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.py') as tmp_file:
            tmp_file.write(code.encode('utf-8'))
            tmp_file_path = tmp_file.name
        
        result = subprocess.run(
            ['python', tmp_file_path],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        os.remove(tmp_file_path)
        
        return jsonify({
            'stdout': result.stdout,
            'stderr': result.stderr
        })
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Execution timed out'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
