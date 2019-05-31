from mygene import MyGeneInfo
from .Mod0_disease_gene_lookup import LookUp
import asyncio

from collections import namedtuple

class GeneSetWrapper(object):

    def __init__(self, taxon='human') -> None:
        self.taxon = taxon
        self.mgi = MyGeneInfo()

        self.input_object = []
        self.AnnotatedGene = namedtuple('AnnotatedGene', ['gene_symbol', 'input_id', 'sim_input_curie'])

    def load_gene(self, biolinkGeneHit):

        gene_symbol = None
        gene_id = None
        input_id = None

        if 'MGI' in biolinkGeneHit['hit_id']:
            gene_id = biolinkGeneHit['hit_id']
            input_id = biolinkGeneHit['hit_id']

        elif 'HGNC' in biolinkGeneHit['hit_id']:
            try:

                hgnc_hit = self.hgncCurie2hgncHit(biolinkGeneHit['hit_id'])
                input_id = hgnc_hit["input_id"]
                gene_id = hgnc_hit["input_id"] # not uniprot id === gene_id?
                gene_symbol = hgnc_hit["gene_symbol"]

            except Exception as e:
                print(biolinkGeneHit, e)

        # TODO: convert to a namedtuple passing through instead of an _asdict() -> OrderedDict -> Dict
        # TODO: how is this different from the biolinkGeneHit?
        return dict(self.AnnotatedGene(gene_symbol, gene_id, input_id)._asdict())

    def load_gene_set(self, gene_identifiers):
        print("gene identifiers", gene_identifiers)
        annotated_gene_set = []
        for gene in gene_identifiers:
            annotated_gene = self.load_gene(gene)
            annotated_gene_set.append(annotated_gene)
        return annotated_gene_set

    def symbol2hgnc(self, symbol):
        try:
            mgi_results = self.mgi.query('symbol:' + symbol,
                                   fields='HGNC, symbol, taxon',
                                   species='human',
                                   entrezonly=True)
            if mgi_results['total'] == 1:
                return 'HGNC:' + mgi_results['hits'][0]['HGNC']
            else:
                return False
        except Exception as e:
            print(symbol, e)

    def hgncCurie2hgncHit(self, mgi_gene_curie):
        # MyGeneInfo represents their HGNC identifiers in lowercase
        mgi_gene_curie = mgi_gene_curie.replace('HGNC', 'hgnc')
        scope = 'HGNC'

        try:
            mgi_results = self.mgi.query(mgi_gene_curie,
                                          scopes=scope,
                                          species=self.taxon,
                                          fields='symbol, uniprot, HGNC',
                                          entrezonly=True)

            # If there is going to be a hit, there is only going to be one hit, because we are querying by
            # what is meant to be a unique identifier
            myGeneInfoHit = [
                {
                    "input_id": "HGNC:" + result["HGNC"],
                    # TODO: does this make sense?
                    #  result["uniprot"]["Swiss-Prot"] if result["uniprot"]["Swiss-Prot"] else "HGNC:" + result["HGNC"],
                    "gene_id":"HGNC:" + result["HGNC"],
                    "gene_symbol": result["symbol"]
                }
                for result in mgi_results['hits']
            ][0]
            
            return myGeneInfoHit

        except Exception as e:
            print(mgi_gene_curie, e)

