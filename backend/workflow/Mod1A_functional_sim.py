from .generic_similarity import GenericSimilarity
from pprint import pprint

class FunctionalSimilarity(GenericSimilarity):

    def __init__(self, taxon, threshold):
        GenericSimilarity.__init__(self, taxon, threshold)

        self.input_object = ''
        self.ont = 'go'
        self.meta = {
            'input_type': {
                'complexity': 'set',
                'id_type': 'HGNC',
                'data_type': 'gene',
            },
            'output_type': {
                'complexity': 'set',
                'id_type': 'HGNC',
                'data_type': 'gene',
            },

            'source': 'Monarch Biolink',
            'predicate': ['blm:macromolecular machine to biological process association',
                          'macromolecular machine to molecular activity association']
        }

        # Load the functional catalog of
        # GO ontology and annotation associations
        self.load_associations(self.taxon)

    def metadata(self):
        print("""Mod1A Functional Similarity metadata:""")
        pprint(self.meta)

    def load_gene(self, biolinkGeneHit):

        gene_symbol = None
        gene_id = None
        input_id = None

        if 'MGI' in biolinkGeneHit['hit_id']:

            gene_id = biolinkGeneHit['hit_id']
            input_id = biolinkGeneHit['hit_id']

        elif 'HGNC' in biolinkGeneHit['hit_id']:

            # MyGeneInfo represents their HGNC identifiers in lowercase
            mgi_gene_curie = biolinkGeneHit['hit_id'].replace('HGNC', 'hgnc')
            scope = 'HGNC'

            try:
                mgi_results = self.mgi.query(mgi_gene_curie,
                                             scopes=scope,
                                             species=self.taxon,
                                             fields='symbol, uniprot, HGNC',
                                             entrezonly=True)

                # myGeneInfoHits = []
                # for i in range(0, len(mgi_results['hits'])):
                #     myGeneInfoHits.append(
                #         self.MyGeneInfoHit(mgi_results['hits'][i]['symbol'],
                #                            mgi_results['hits'][i]['uniprot'],
                #                            mgi_results['hits'][i]['HGNC'])
                #     )

                gene_id = biolinkGeneHit['hit_id']
                input_id = 'UniProtKB:{}'.format(mgi_results['hits'][0]['uniprot']['Swiss-Prot'])

            except Exception as e:
                print(biolinkGeneHit, e)

        # TODO: convert to a namedtuple passing through instead of an _asdict() -> OrderedDict -> Dict
        # TODO: how is this different from the biolinkGeneHit?
        return dict(self.AnnotatedGene(gene_symbol, gene_id, input_id)._asdict())

    def compute_similarity(self):
        group = self.input_object['parameters']['taxon']
        lower_bound = float(self.input_object['parameters']['threshold'])
        results = self.compute_jaccard(self.gene_set, lower_bound)
        for result in results:
            if group == 'human':
                result['hit_id'] = self.symbol2hgnc(result['hit_symbol'])
            for gene in self.gene_set:
                if gene['sim_input_curie'] != result['input_id']:
                    result['input_id'] = self.symbol2hgnc(result['input_symbol'])
        return results