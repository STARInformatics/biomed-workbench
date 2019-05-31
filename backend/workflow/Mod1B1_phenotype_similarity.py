from mygene import MyGeneInfo
from .generic_similarity import GenericSimilarity
from pprint import pprint

class PhenotypeSimilarity(GenericSimilarity):

    def __init__(self, taxon, threshold):
        GenericSimilarity.__init__(self, taxon, threshold)

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
        self.load_associations(self.taxon)

    def metadata(self):
        print("""Mod1B1 Phenotype Similarity metadata:""")
        pprint(self.meta)