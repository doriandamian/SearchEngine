from flask import Flask, request, jsonify
from flask_cors import CORS
from file_database import FileDatabase

app = Flask(__name__)
db = FileDatabase()
CORS(app)

@app.route('/search', methods=['GET'])
def search_files():
    query = request.args.get('query', '')
    
    if not query:
        return jsonify([])

    result = db.searchFiles(query)

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)