from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Retrieve the API key from environment variables
API_KEY = os.getenv('API_KEY')

@app.route('/', methods=['GET'])
def index():
    category = request.args.get('category', 'general')
    country = request.args.get('country', 'us')
    url = f'https://newsapi.org/v2/top-headlines?country={country}&category={category}&apiKey={API_KEY}'
    response = requests.get(url)
    articles = response.json().get('articles', [])
    return render_template('index.html', articles=articles, category=category, country=country)

if __name__ == '__main__':
    app.run(debug=True)
