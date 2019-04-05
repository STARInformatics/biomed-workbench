import json, os
from functools import lru_cache
from typing import List

MONDO = 'http://purl.obolibrary.org/obo/MONDO_'

def get(d:dict, *keys:str, default=None):
    try:
        for key in keys:
            d = d[key]
        return d
    except:
        return default

@lru_cache()
def load_mondo():
    path = os.path.dirname(os.path.abspath(__name__))
    with open(f'{path}/server/data/mondo.json', 'r') as f:
        d = json.load(f)
        results = {}
        for graph in d['graphs']:
            for node in graph['nodes']:
                if MONDO in node['id']:
                    if 'lbl' not in node:
                        continue
                    if get(node, 'meta', 'deprecated') is True:
                        continue
                    synonoms = [syn['val'].lower() for syn in get(node, 'meta', 'synonyms', default=[])]
                    curie = node['id'].replace(MONDO, 'MONDO:')
                    # import pudb; pu.db
                    results[curie] = {
                        'iri' : node['id'],
                        'definition' : get(node, 'meta', 'definition', 'val'),
                        'synonoms' : synonoms,
                        'name' : node['lbl'].lower(),
                    }
        return results

def search(keywords:List[str]) -> List[dict]:
    if isinstance(keywords, str):
        keywords = keywords.lower().split()
    elif isinstance(keywords, (list, tuple, set)):
        keywords = [k.lower() for k in keywords]
    else:
        raise Exception(f'Invalid type {type(keywords)} for keywords')

    nodes = load_mondo()
    results = []
    for curie, node in nodes.items():
        node['id'] = curie
        for keyword in keywords:
            if keyword in node['name']:
                results.append(node)
                break

    def keyword_order(node):
        synonoms = node['synonoms'] + [node['name']]
        m = min(-sum(synonom.count(keyword) / len(synonom) for keyword in keywords) for synonom in synonoms)
        return m

    def exact_term_order(node):
        synonoms = node['synonoms'] + [node['name']]
        k = ' '.join(keywords)
        s = -sum(synonom.count(k) for synonom in synonoms)
        if node['name'] == k:
            s -= 1
        return s

    results = sorted(results, key=keyword_order)
    results = sorted(results, key=exact_term_order)

    return results
