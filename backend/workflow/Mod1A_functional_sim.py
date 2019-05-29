from .generic_similarity import GenericSimilarity
from .gene_set import GeneSet
from pprint import pprint

class FunctionalSimilarity(GenericSimilarity, GeneSet):

    def __init__(self, taxon):
        GenericSimilarity.__init__(self)
        self.input_object = ''
        self.taxon = taxon
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
        self.load_associations(taxon)

    def metadata(self):
        print("""Mod1A Functional Similarity metadata:""")
        pprint(self.meta)

    def compute_similarity(self, annotated_gene_set, threshold):
        lower_bound = float(threshold)
        results = self.compute_jaccard(annotated_gene_set, lower_bound)
        for result in results:
            if self.taxon == 'human':
                result['hit_id'] = self.symbol2hgnc(result['hit_symbol'])
            for gene in annotated_gene_set:
                if gene['sim_input_curie'] != result['input_id']:
                    result['input_id'] = self.symbol2hgnc(result['input_symbol'])
        return results




