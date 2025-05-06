import secrets

api_keys_cache = {}

def generate_api_key():
    while True:
        new_key = secrets.token_hex(16)
        if new_key not in api_keys_cache:
            api_keys_cache[new_key] = True
            return new_key

def get_all_api_keys():
    readable_keys = []
    for index, key in enumerate(api_keys_cache.keys(), start=1):
        readable_keys.append(f"{index}. {key}")
    return "\n".join(readable_keys)

def is_valid_api_key(api_key):
    return api_key in api_keys_cache