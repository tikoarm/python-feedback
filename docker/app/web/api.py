from flask import Flask, jsonify, request
import asyncio
from database.reviews import get_all_reviews, get_user_reviews

app = Flask(__name__)

@app.route('/review_list/')
def review_list():
    user_param = request.args.get('user', default='all')

    if user_param == "all": 
        reviews = asyncio.run(get_all_reviews())
    else:
        try:
            user_id = int(user_param)
        except ValueError:
            return jsonify({"error": "Invalid user ID"}), 400

        reviews = asyncio.run(get_user_reviews(user_id))
    
    return jsonify(reviews)

def start_api():
    app.run(host='0.0.0.0', port=5050)