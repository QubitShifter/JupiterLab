import re
from Utils.Dicts.dict_Es_to_En import es_to_en_map


def translator(text):
    if not isinstance(text, str):
        return text

    text = re.sub(r'\ba\b', 'to', text, flags=re.IGNORECASE )

    for spanish, english in es_to_en_map.items():
        text = re.sub(rf'\b{spanish}\b', english, text, flags=re.IGNORECASE)
    return text


test_string = "Mayo a Julio"
#print(translator(test_string))
