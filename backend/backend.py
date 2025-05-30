from parser import Parser
from file_database import FileDatabase
from spelling_corrector import correction
from widgets.widget_factory import WidgetFactory
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="*")

db = FileDatabase()
widget_factory = WidgetFactory()

@app.route("/history", methods=["GET"])
def get_search_history():
    recent_searches = db.getSearches()
    return jsonify(recent_searches)


@app.route("/search", methods=["GET"])
def search_files():
    paths = request.args.getlist("path")
    titles = request.args.getlist("title")
    extensions = request.args.getlist("extension")
    contents = request.args.getlist("contents")

    queries = []
    for path in paths:
        if path.strip():
            queries.append(f"path:{path.strip()}")
            db.insertSearch(path.strip(), "path")
    for title in titles:
        if title.strip():
            corrected = correction(title.strip())
            queries.append(f"title:{corrected}")
            db.insertSearch(corrected, "title")
    for extension in extensions:
        if extension.strip():
            queries.append(f"extension:{extension.strip()}")
            db.insertSearch(extension.strip(), "extension")
    for content in contents:
        if content.strip():
            corrected = correction(content.strip())
            queries.append(f"content:{corrected}")
            db.insertSearch(corrected, "content")

    if not queries:
        return jsonify({"error": "No query found"}), 400

    query = " ".join(queries)
    query = Parser.parseQuery(query)
    result = db.searchFiles(query)

    widgets = widget_factory.get_widgets(query, result)

    return jsonify({
        "result":result,
        "widgets": widgets    
    }), 200

if __name__ == "__main__":
    app.run(debug=True)
