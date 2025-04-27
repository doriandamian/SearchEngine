from flask import Flask, request, jsonify
from flask_cors import CORS
from file_database import FileDatabase

from parser import Parser

app = Flask(__name__)
CORS(app)

db = FileDatabase()

@app.route('/search', methods=['GET'])
def search_files():
    paths = request.args.getlist('path')
    titles = request.args.getlist('title')
    extensions = request.args.getlist('extension')
    contents = request.args.getlist('contents')
    
    queries = []
    for path in paths:
        if path.strip():
            queries.append(f"path:{path.strip()}")
    for title in titles:
        if title.strip():
            queries.append(f"title:{title.strip()}")
            db.insertSearch(title.strip())
    for extension in extensions:
        if extension.strip():
            queries.append(f"extension:{extension.strip()}")
    for content in contents:
        if content.strip():
            queries.append(f"content:{content.strip()}")
            db.insertSearch(content.strip())

    if not queries:
        return jsonify({"error": "No query found"}), 400

    query = " ".join(queries)
    query = Parser.parseQuery(query)
    result = db.searchFiles(query)

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)