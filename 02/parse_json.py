import json


def parse_json(json_str: str, keyword_callback, required_fields=None, keywords=None):
    def json_process():
        json_doc = json.loads(json_str)

        for field in required_fields:
            if field in json_doc.keys():
                for word in keywords:
                    if word.lower() in list(set(json_doc[field].lower().split())):
                        keyword_callback(field, word)

    if callable(keyword_callback):
        if keywords is not None and required_fields is not None:
            json_process()
    else:
        raise TypeError("keyword_callbac должна быть функцией")

    if keywords is None or required_fields is None:
        pass


