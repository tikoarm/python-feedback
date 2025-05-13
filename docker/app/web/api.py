import asyncio
import os

from cache import api_keys
from database.reviews import get_all_reviews, get_user_reviews
from dotenv import dotenv_values, load_dotenv
from flask import Flask, jsonify, request

load_dotenv()
admin_key = os.getenv("API_ADMIN_KEY")
if not admin_key:
    raise ValueError(
        "Missing API Admin Key credential in environment variables."
    )

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


@app.route("/logs/view", methods=["GET"])
def logs_view_process():
    admkey_param = request.args.get("admin_key")
    if not admkey_param:
        return jsonify({"error": "Admin Key is required"}), 400

    adm_key = admkey_param.strip()
    if adm_key != admin_key:
        error_message = f"Admin Key '{adm_key}' is Invalid!"
        return jsonify({"error": error_message}), 400

    logtype_param = request.args.get("log_type")
    if not logtype_param:
        return jsonify({"error": "Log Type is required"}), 400

    try:
        env_values = dotenv_values()
    except Exception:
        env_values = {}

    sensitive_values = list(
        {
            v
            for v in list(env_values.values()) + list(os.environ.values())
            if v and len(v) >= 6
        }
    )

    # Mask sensitive values in log lines
    def mask_sensitive(line, sensitive_values):
        for value in sensitive_values:
            if value and value in line:
                line = line.replace(value, "--hidden--")
        return line

    log_files = {
        "error": "logs/error.log",
        "warning": "logs/warning.log",
        "info": "logs/info.log",
    }

    if logtype_param not in log_files:
        return jsonify({"error": "Log Type is incorrect"}), 400

    file_path = log_files[logtype_param]
    try:
        with open(file_path, "r") as f:
            raw_lines = f.readlines()
            masked_lines = [
                mask_sensitive(line, sensitive_values) for line in raw_lines
            ]
            lines = masked_lines[-25:]

    except FileNotFoundError:
        return (
            jsonify({"error": f"Log file for '{logtype_param}' not found"}),
            404,
        )

    return jsonify({"log_type": logtype_param, "lines": lines})


@app.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint returning status of key components and version.
    """
    result = {'status': 'ok'}

    # 1) Version
    version_path = os.path.join(os.getcwd(), 'VERSION')
    try:
        with open(version_path, 'r') as f:
            result['version'] = f.read().strip()
    except Exception:
        result['version'] = 'unknown'
        result['status'] = 'degraded'

    # 2) Database
    try:
        from database.connection import get_connection
        conn = get_connection()
        conn.close()
        result['database'] = 'ok'
    except Exception as e:
        result['database'] = f'error: {e}'
        result['status'] = 'degraded'

    return jsonify(result)


def start_api():
    app.run(host="0.0.0.0", port=5050, debug=False)  # nosec
