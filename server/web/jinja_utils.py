import json


def json_loads(json_str: str):
    return json.loads(json_str)


def cstm_context_processor():
    return dict(json_loads=json_loads)
