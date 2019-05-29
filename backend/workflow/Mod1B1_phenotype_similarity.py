from mygene import MyGeneInfo
from .generic_similarity import GenericSimilarity
from .gene_set import GeneSet
from pprint import pprint

class PhenotypeSimilarity(GenericSimilarity, GeneSet):

    def __init__(self, taxon):
        GenericSimilarity.__init__(self)
        self.taxon = taxon
        if self.taxon == 'mouse':
            self.ont = 'mp'
        if self.taxon == 'human':
            self.ont = 'hp'
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
            'predicate': ['blm:has phenotype']
        }

        # Load the associated Biolink (Monarch)
        # phenotype ontology and annotation associations
        self.load_associations(taxon)

    def metadata(self):
        print("""Mod1B1 Phenotype Similarity metadata:""")
        pprint(self.meta)

    def compute_similarity(self, annotated_gene_set, threshold):
        lower_bound = float(threshold)
        results = self.compute_jaccard(annotated_gene_set, lower_bound)
        for result in results:
            for gene in annotated_gene_set:
                if gene['sim_input_curie'] == result['input_id']:
                    result['input_symbol'] = gene['input_symbol']
        return results
