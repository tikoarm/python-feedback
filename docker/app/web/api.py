from flask import Flask, jsonify, request
import asyncio
import os
from dotenv import load_dotenv

from database.reviews import get_all_reviews, get_user_reviews
from cache import api_keys

load_dotenv()
admin_key = os.getenv("API_ADMIN_KEY")
if not admin_key:
    raise ValueError("Missing API Admin Key credential in environment variables.")

app = Flask(__name__)


@app.route("/review_list/")
def review_list():
    apikey_param = request.args.get("api_key")
    if not apikey_param:
        return jsonify({"error": "API key is required"}), 400
    api_key = apikey_param.strip()
    if not api_keys.is_valid_api_key(api_key):
        error_message = f"Key '{api_key}' is Invalid!"
        return jsonify({"error": error_message}), 400

    user_param = request.args.get("user", default="all")
    if user_param == "all":
        reviews = asyncio.run(get_all_reviews())
    else:
        try:
            user_id = int(user_param)
        except ValueError:
            return jsonify({"error": "Invalid user ID"}), 400

        reviews = asyncio.run(get_user_reviews(user_id))

    return jsonify(reviews)


@app.route("/apikey/add", methods=["POST"])
def add_api_key():
    admkey_param = request.args.get("admin_key")
    if not admkey_param:
        return jsonify({"error": "Admin Key is required"}), 400

    adm_key = admkey_param.strip()
    if adm_key != admin_key:
        error_message = f"Admin Key '{adm_key}' is Invalid!"
        return jsonify({"error": error_message}), 400

    user_param = request.args.get("user_id")
    if not user_param:
        return jsonify({"error": "User ID is required"}), 400

    try:
        user_id = int(user_param)
    except ValueError:
        return jsonify({"error": "Invalid user ID"}), 400

    new_api_key = asyncio.run(api_keys.generate_api_key(user_id))
    return jsonify({"api_key": new_api_key})


def start_api():
    app.run(host="0.0.0.0", port=5050, debug=False)  # nosec
