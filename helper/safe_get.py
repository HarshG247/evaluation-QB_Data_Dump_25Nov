# Helper function to safely extract nested dictionary values
def safe_get(dictionary, keys, default=""):
    try:
        for key in keys:
            dictionary = dictionary.get(key, {})
        return dictionary if isinstance(dictionary, str) else default
    except AttributeError:
        return default
