from flask import Flask, jsonify
import asyncio
from database.reviews import get_all_reviews

app = Flask(__name__)

@app.route('/review_list/')
def review_list():
    reviews = asyncio.run(get_all_reviews()) 
    return jsonify(reviews)

def start_api():
    app.run(host='0.0.0.0', port=5050)