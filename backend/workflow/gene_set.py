from mygene import MyGeneInfo
from .Mod0_disease_gene_lookup import LookUp

class GeneSet(object):
    def __init__(self) -> None:
        pass

    def load_gene(self, geneKey):
        mg = MyGeneInfo()
        gene_curie = ''
        sim_input_curie = ''
        symbol = ''

        if 'MGI' in geneKey['hit_id']:
            gene_curie = geneKey['hit_id']
            sim_input_curie = geneKey['hit_id']
            symbol = None
        if 'HGNC' in geneKey['hit_id']:
            mgi_gene_curie = geneKey['hit_id'].replace('HGNC', 'hgnc')
            scope = 'HGNC'
            try:
                mg_hit = mg.query(mgi_gene_curie,
                                  scopes=scope,
                                  species=self.taxon,
                                  fields='uniprot, symbol, HGNC',
                                  entrezonly=True)
                gene_curie = geneKey['hit_id']
                sim_input_curie = geneKey['hit_id']
                symbol = mg_hit['hits'][0]['symbol']
            except Exception as e:
                print(geneKey, e)

        annotated_gene = {
            'input_id': gene_curie,
            'sim_input_curie': sim_input_curie,
            'input_symbol': symbol #geneKey['hit_symbol']
        }
        return annotated_gene

    def load_gene_set(self, input_gene_set):
        annotated_gene_set = []
        for gene in input_gene_set.get_input_curie_set():
            annotated_gene = self.load_gene(gene)
            annotated_gene_set.append(annotated_gene)
        return annotated_gene_set

    def symbol2hgnc(self, symbol):
        mg_hit = self.mg.query('symbol:{}'.format(symbol),
                               fields='HGNC,symbol,taxon',
                               species='human',
                               entrezonly=True)
        if mg_hit['total'] == 1:
            return 'HGNC:{}'.format(mg_hit['hits'][0]['HGNC'])

class DiseaseAssociatedGeneSet(object):

    def __init__(self, input_disease_symbol, input_disease_mondo):
        self.input_disease_symbol = input_disease_symbol
        self.input_disease_mondo = input_disease_mondo

        # TODO: refactor away from LU
        # workflow input is a disease identifier
        self.lu = LookUp()

        input_object = {
            'input': self.input_disease_mondo,
            'parameters': {
                'taxon': 'human',
                'threshold': None,
            },
        }

        self.lu.load_input_object(input_object=input_object)

        # get genes associated with disease from Biolink
        self.disease_associated_genes = self.lu.disease_geneset_lookup()

        self.input_curie_set = self.disease_associated_genes[['hit_id', 'hit_symbol']].to_dict(orient='records')

    # TODO: refactor away from LU
    def echo_input_object(self, output=None):
        return self.lu.echo_input_object(output)

    # TODO: refactor away from LU
    def get_input_object_id(self):
        return self.lu.get_input_object_id()

    def get_input_disease_symbol(self):
        return self.input_disease_symbol

    def get_data_frame(self):
        return self.disease_associated_genes

    def get_input_curie_set(self):
        return self.input_curie_set
