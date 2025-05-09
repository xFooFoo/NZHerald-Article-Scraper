from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from NZHScraperFlask import scrapeContent


app = Flask(__name__)
CORS(app) 

@app.route('/', methods=['GET'])
def home():
    return 'Backend is running ✅✅✅', 200

@app.route('/api/submit', methods=['POST'])
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

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True)