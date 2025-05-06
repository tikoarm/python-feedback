from flask import Flask, jsonify, request
import asyncio
from database.reviews import get_all_reviews, get_user_reviews
from cache import api_keys

app = Flask(__name__)

@app.route('/review_list/')
def review_list():
    apikey_param = request.args.get('api_key')
    if not apikey_param:
        return jsonify({"error": "API key is required"}), 400
    api_key = apikey_param.strip()
    if not api_keys.is_valid_api_key(api_key):
        error_message = f"Key '{api_key}' is Invalid! valids: {api_keys.get_all_api_keys()}"
        return jsonify({"error": error_message}), 400
    

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