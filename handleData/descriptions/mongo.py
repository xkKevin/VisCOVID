from functools import reduce
from ..parser.parser import get_parser
def load_descriptions(ids, db, config):
    parser = get_parser()
    descriptions = list(filter(lambda x: not not x, map(lambda did: db.descriptions.find_one({"id": did}), ids)))
    print(descriptions)
    descriptions = list(map(parser.parse_description, descriptions))
    ids = list(map(lambda x: x['id'], descriptions))
    def f(acc, c):
        acc[c['id']] = c
        return acc
    descriptions_index = reduce(f, descriptions, {})
    return descriptions_index, ids