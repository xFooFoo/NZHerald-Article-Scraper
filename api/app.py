from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from NZHScraperFlask import scrapeContent
import os


app = Flask(__name__, static_folder='../frontend/build', static_url_path='')
CORS(app, resources={r"/api/*": {"origins": "*"}}) 

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html'), 200 # React Entry point

# This serves JS, CSS, manifest, etc.
@app.route('/<path:path>')
def serve_static_file(path):
    file_path = os.path.join(app.static_folder, path)
    if os.path.exists(file_path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.route('/submit', methods=['POST'])
def scrape_data():
    try:
        data = request.get_json()  # Get the JSON data from the request body
        url = data.get('url')  # Access the value sent from React
        title, content = scrapeContent(url)

        # You can now process the data (e.g., store in a database, etc.)
        print(f"Received value: {url}")
        
        # Respond with a success message
        return jsonify({
            "fetchStatus": "Article scraped successfully!!! 😁😁😁",
            "title": title,
            "content": content
        }), 200
    except Exception as e:
        return jsonify({"fetchStatus": f"Error: Invalid URL {url} 💀💀💀"}), 500

# if __name__ == '__main__':
#     print("Starting Flask server...")
#     app.run()