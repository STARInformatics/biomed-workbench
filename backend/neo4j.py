import grequests

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

def get_statements(curie:str) -> dict:
    # https://neo4j.com/docs/rest-docs/current/#rest-api-use-parameters
    curie = curie.replace('`', '').replace('"', '').replace("'", '')
    q = """
    match (n)-[e]-(m) where
        toLower(n.id) = toLower('{curie}')
    return
        n,
        e,
        m,
        EXISTS((n)-[e]->(m)) as isSubject
    limit 100;
    """.format(curie=curie)

    print(q)

    data = {"query" : q}

    requests = []

    for uri, auth in db.items():
        requests.append(grequests.post(uri + base_path, data=data, auth=auth, timeout=60000))

    responses = grequests.map(requests)

    statements = []

    from pprint import pprint
    for response in responses:
        if response is None:
            continue
        data = response.json().get('data', [])
        data = [[parse(d) for d in record] for record in data]
        for source, edge, target, isSourceSubject in data:
            if isSourceSubject:
                statements.append({
                    'subject' : source,
                    'edge' : edge,
                    'object' : target,
                })
            else:
                statements.append({
                    'subject' : target,
                    'edge' : edge,
                    'object' : source,
                })
    return statements


if __name__ == '__main__':
    from pprint import pprint
    pprint(get_statements('HP:0000212'))
