import json
import re


def get_data(path):
    with open(path) as f:
        data = f.read()
    if path.endswith('.json'):
        return json.loads(data)
    elif path.endswith('.tz'):
        return re.sub('\n\s*', ' ', data)
    else:
        assert False, path
