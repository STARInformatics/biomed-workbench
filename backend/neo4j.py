import grequests
import bmt

db = {
    'http://34.229.55.225:7474' : ('neo4j', 'VQH39pWYopKIzmiv'),
    'http://scigraph.ncats.io' : ('neo4j', 'neo4j'),
    'http://steveneo4j.saramsey.org:7474' : ('neo4j', 'precisionmedicine'),
    'http://robokopdb2.renci.org:7474' : ('neo4j' , 'ncatsgamma'),
}

base_path = '/db/data/cypher'

def parse(d:dict):
    if isinstance(d, dict):
        data = d.get('data')
        metadata = d.get('metadata')
        if 'type' in metadata:
            data['type'] = metadata['type']
        if 'labels' in metadata:
            data['labels'] = metadata['labels']
        return data
    else:
        return d

def get_ncats_data(curie:str) -> dict:
    """
    Gets the concept identified by the given curie, as well as all statements
    it is involved in.
    """
    q = """
    match (n)
    where toLower(n.id) = toLower('{curie}')
    match (n)-[e]-(m)
    with n, e, m limit 100
    return n AS source, COLLECT({{edge:e, target:m, sourceIsSubject: EXISTS((n)-[e]->(m))}}) as edges
    """.format(curie=curie)

    print(q)

    data = {"query" : q}

    requests = []

    for uri, auth in db.items():
        requests.append(grequests.post(uri + base_path, data=data, auth=auth, timeout=60000))

    responses = grequests.map(requests)

    statements = []
    sources = []

    for response in responses:
        if response is None:
            continue
        data = response.json().get('data', [])
        data = [[parse(d) for d in record] for record in data]

        for source, edges in data:
            sources.append(source)
            for relation in edges:
                edge = parse(relation.get('edge', {}))
                target = parse(relation.get('target', {}))
                sourceIsSubject = relation.get('sourceIsSubject')

                if sourceIsSubject is True:
                    statements.append({
                        'subject' : source,
                        'edge' : edge,
                        'object' : target,
                    })
                elif sourceIsSubject is False:
                    statements.append({
                        'subject' : target,
                        'edge' : edge,
                        'object' : source,
                    })
                else:
                    raise Exception('Invalid value for sourceIsSubject: {}'.format(sourceIsSubject))

    concept = {}
    for source in sources:
        for key, value in source.items():
            if key not in concept:
                concept[key] = value

    for key, value in concept.items():
        if isinstance(value, list):
            concept[key] = list(set(value))

    if 'category' not in concept:
        category = []
    elif isinstance(concept['category'], str):
        category = [concept['category']]
    elif isinstance(concept['category'], list):
        category = concept['category']

    for label in concept.get('labels', []):
        e = bmt.get_element(label)
        if e is not None:
            category.append(e.name)
    concept['category'] = list(set(category))

    return {
        'concept' : concept,
        'statements' : statements,
    }


if __name__ == '__main__':
    from pprint import pprint
    d = get_ncats_data('HP:0000212')

    print('Sources:')
    pprint(d['sources'])
    print('Statements (first five):')
    pprint(d['statements'][:5])
