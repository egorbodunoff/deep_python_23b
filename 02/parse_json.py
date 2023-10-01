import json


def parse_json(json_str: str, keyword_callback, required_fields=None, keywords=None):
    json_doc = json.loads(json_str)

    json_fields = {x: json_doc[x].split() for x in json_doc if x in required_fields}
    json_words = [elem for inner_list in list(json_fields.values()) for elem in inner_list]
    words = set([word for word in json_words if word in keywords])

    for word in list(words):
        keyword_callback(word)
