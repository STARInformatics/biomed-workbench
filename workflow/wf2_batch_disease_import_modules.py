# Imports
from pprint import pprint
from sys import stdout
from json import dump
from typing import List, Union, TextIO
from datetime import datetime

from ontobio.assocmodel import AssociationSet
from ontobio.ontol_factory import OntologyFactory
from ontobio.io.gafparser import GafParser
from ontobio.assoc_factory import AssociationSetFactory
from ontobio.analysis.semsim import jaccard_similarity
from mygene import MyGeneInfo
import pandas as pd

import requests


# BioLink submodule
class BioLinkWrapper(object):
    def __init__(self):
        self.endpoint = 'https://api.monarchinitiative.org/api/'
        self.params = {
            'fetch_objects': 'true',
        }

    def get_obj(self, obj_id):
        url = '{0}bioentity/{1}'.format(self.endpoint, obj_id)
        response = requests.get(url)
        return response.json()

    def disease2genes(self, disease_curie):
        params = {}
        params.update(self.params)
        url = '{0}bioentity/disease/{1}/genes'.format(self.endpoint, disease_curie)
        response = requests.get(url, params)
        return response.json()

    def disease2phenotypes(self, disease_curie):
        params = {}
        url = '{0}bioentity/disease/{1}/phenotypes'.format(self.endpoint, disease_curie)
        response = requests.get(url, params)
        return response.json()

    def gene(self, gene_curie):
        params = {}
        url = '{0}bioentity/gene/{1}'.format(self.endpoint, gene_curie)
        response = requests.get(url, params)
        return response.json()

    def gene2orthologs(self, gene_curie, orth_taxon_name=None):
        taxon_map = {
            'human': 'NCBITaxon:9606',
            'mouse': 'NCBITaxon:10090',
            'rat': 'NCBITaxon:10116',
            'zebrafish': 'NCBITaxon:7955',
            'fly': 'NCBITaxon:7227',
            'worm': 'NCBITaxon:6239'
        }
        params = {}
        if orth_taxon_name:
            params['homolog_taxon'] = taxon_map[orth_taxon_name]
        url = '{}bioentity/gene/{}/homologs'.format(self.endpoint, gene_curie)
        response = requests.get(url, params)
        return response.json()

    def phenotype2genes(self, phenotype_curie):
        url = '{}bioentity/phenotype/{}/genes'.format(self.endpoint, phenotype_curie)
        response = requests.get(url)
        return response.json()

    def gene2phenotypes(self, gene_curie):
        url = '{}bioentity/gene/{}/phenotypes'.format(self.endpoint, gene_curie)
        response = requests.get(url)
        return response.json()

    def gene2diseases(self, gene_curie):
        url = '{}bioentity/gene/{}/diseases'.format(self.endpoint, gene_curie)
        response = requests.get(url)
        return response.json()

    def gene_interactions(self, gene_curie):
        url = '{}bioentity/gene/{}/interactions'.format(self.endpoint, gene_curie)
        response = requests.get(url)
        return response.json()

    def gene2functions(self, gene_curie):
        url = '{}bioentity/gene/{}/function'.format(self.endpoint, gene_curie)
        response = requests.get(url)
        return response.json()

    def gene2tissue_expression(self, gene_curie):
        url = '{}bioentity/gene/{}/expression/anatomy'.format(self.endpoint, gene_curie)
        response = requests.get(url)
        return response.json()

    def tissue2gene_expression(self, tissue_curie):
        url = '{}bioentity/anatomy/{}/genes'.format(self.endpoint, gene_curie)
        response = requests.get(url)
        return response.json()

    def disease_models(self, disease_curie):
        url = '{}/bioentity/disease/{}/models'.format(self.endpoint, disease_curie)
        response = requests.get(url)
        return response.json()

    def taxon2phenotypes(self, taxon_curie):
        # get phenotypes associated with taxid
        url = "mart/gene/phenotype/{}".format(self.endpoint, taxon_curie)
        response = requests.get(url)
        return response.json()

    def parse_gene_functions(self, curie):
        function_list = list()
        functions = self.gene2functions(gene_curie=curie)
        if 'associations' in functions.keys():
            for assoc in functions['associations']:
                function_list.append(assoc['object']['label'])
        function_set = set(function_list)
        return ", ".join(function_set)

    def get_orthoglog_gene_set(self, gene_set, orth_taxon_name):
        orth_set = []
        for gene in gene_set:
            orth_set.append(self.gene2orthologs(gene_curie=gene, orth_taxon_name=orth_taxon_name))
        return orth_set

    def compute_jaccard(self, id1, id2, category):
        url = "{0}/pair/sim/jaccard/{1}/{2}/".format(self.endpoint, id1, id2)
        params ={
            'object_category': category
        }
        params.update(self.params)
        response = requests.get(url, params)
        return response.json()

    def compute_owlsim(self, id):
        url = '{0}sim/search'.format(self.endpoint)
        params = {
            'id': id,
        }
        params.update(self.params)
        response = requests.get(url, params)
        return response.json()

    @staticmethod
    def parse_sources(sources):
        return [x.split('/')[-1].rstrip('.ttl') for x in sources]

    @staticmethod
    def parse_association(input_id, input_label, association, invert_subject_object=False):
        hit_id = association['object']['id']
        hit_label = association['object']['label']
        relation_label = association['relation']['label']
        if invert_subject_object:
            hit_id = association['subject']['id']
            hit_label = association['subject']['label']

        parsed_association = {
            'input_id': input_id,
            'input_symbol': input_label,
            'hit_id': hit_id,
            'hit_symbol': hit_label,
            'sources': BioLinkWrapper.parse_sources(association['provided_by']),
            'relation': relation_label
        }
        return parsed_association

    @staticmethod
    def return_objects(assoc_package):
        return assoc_package['objects']

    @staticmethod
    def filter_on_predicate(package, predicate):
        package['associations'] = [x for x in package['associations'] if x['relation']['label'] == predicate]
        return package


# generic_similarity
class GenericSimilarity(object):
    def __init__(self) -> None:
        self.associations = ''
        self.ontology = ''
        self.assocs = ''
        self.afactory = AssociationSetFactory()

    def retrieve_associations(self, ont, group):
        taxon_map = {
            'human': 'NCBITaxon:9606',
            'mouse': 'NCBITaxon:10090',
        }
        ofactory = OntologyFactory()
        self.ontology = ofactory.create(ont)
        p = GafParser()
        url = ''
        if ont == 'go':
            go_roots = set(self.ontology.descendants('GO:0008150') + self.ontology.descendants('GO:0003674'))
            sub_ont = self.ontology.subontology(go_roots)
            if group == 'mouse':
                url = "http://current.geneontology.org/annotations/mgi.gaf.gz"
            if group == 'human':
                url = "http://current.geneontology.org/annotations/goa_human.gaf.gz"
            assocs = p.parse(url)
            self.assocs = assocs
            assocs = [x for x in assocs if 'header' not in x.keys()]
            assocs = [x for x in assocs if x['object']['id'] in go_roots]
            self.associations = self.afactory.create_from_assocs(assocs, ontology=sub_ont)
        else:
            self.associations = self.afactory.create(ontology=self.ontology ,
                       subject_category='gene',
                       object_category='phenotype',
                       taxon=taxon_map[group])

    def compute_jaccard(self, input_genes:List[dict], lower_bound:float=0.7) -> List[dict]:
        similarities = []
        for index, igene in enumerate(input_genes):
            for subject_curie in self.associations.subject_label_map.keys():
                input_gene = GenericSimilarity.trim_mgi_prefix(input_gene=igene['sim_input_curie'], subject_curie=subject_curie)
                if input_gene is not subject_curie:
                    score = jaccard_similarity(self.associations, input_gene, subject_curie)
                    if float(score) > float(lower_bound):
                        subject_label = self.associations.label(subject_curie)
                        similarities.append({
                            'input_id': input_gene,
                            'input_symbol': igene['input_symbol'],
                            'hit_symbol': subject_label,
                            'hit_id': subject_curie,
                            'score': score,
                        })
        return similarities

    @staticmethod
    def trim_mgi_prefix(input_gene, subject_curie):
        if 'MGI:MGI:' in subject_curie and 'MGI:MGI:' in input_gene:
            return input_gene
        elif 'MGI:MGI:' not in subject_curie and 'MGI:MGI:' in input_gene:
            return input_gene[4:]

        else:
            return input_gene

# Mod0_Lookups
class LookUp(object):

    def __init__(self):
        self.blw = BioLinkWrapper()
        self.mg = MyGeneInfo()
        self.input_object = ''
        self.meta = {
            'data_type': 'disease',
            'input_type': {
                'complexity': 'single',
                'id_type': ['MONDO', 'DO', 'OMIM'],
            },
            'output_type': {
                'complexity': 'set',
                'id_type': 'HGNC'
            },
            'taxon': 'human',
            'limit': None,
            'source': 'Monarch Biolink',
            'predicate': 'blm:gene associated with condition'
        }

    def metadata(self):
        print("""Mod O DiseaseGeneLookup metadata:""")
        pprint(self.meta)

    def load_input_object(self, input_object):
        input_object = self.blw.get_obj(obj_id=input_object['input'])
        self.input_object = {
            'id': input_object['id'],
            'label': input_object['label'],
            'description': input_object['description'],
        }
    
    def echo_input_object(self,output=None):
        if output:
            dump( self.input_object, output, indent=4, separators=(',', ': '))
        else:
            dump( self.input_object, stdout, indent=4, separators=(',', ': '))      

    def disease_geneset_lookup(self):
        input_disease_id = self.input_object['id']
        input_disease_label = self.input_object['label']
        input_gene_set = self.blw.disease2genes(input_disease_id)
        input_gene_set = [self.blw.parse_association(input_disease_id, input_disease_label, x) for x in input_gene_set['associations']]
        # for input_gene in input_gene_set:
        #     igene_mg = self.mg.query(input_gene['hit_id'].replace('HGNC', 'hgnc'), species='human', entrezonly=True,
        #                         fields='entrez,HGNC,symbol')
        #     input_gene.update({'input_ncbi': 'NCBIGene:{}'.format(igene_mg['hits'][0]['_id'])})
        input_genes_df = pd.DataFrame(data=input_gene_set)
        # # group duplicate ids and gather sources
        input_genes_df['sources'] = input_genes_df['sources'].str.join(', ')
        input_genes_df = input_genes_df.groupby(
            ['input_id', 'input_symbol', 'hit_id', 'hit_symbol', 'relation'])['sources'].apply(', '.join).reset_index()
        return input_genes_df



# Mod1A_functional_sim
class FunctionalSimilarity(GenericSimilarity):
    def __init__(self, associations:AssociationSet=None):
        GenericSimilarity.__init__(self)
        self.mg = MyGeneInfo()
        self.gene_set = []
        self.input_object = ''
        self.ont = 'go'
        self.group = ''
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

    def metadata(self):
        print("""Mod1A Functional Similarity metadata:""")
        pprint(self.meta)

    def load_input_object(self, input_object):
        self.input_object = input_object
        if self.input_object['parameters']['taxon'] == 'mouse':
            self.group = 'mouse'
        if self.input_object['parameters']['taxon'] == 'human':
            self.group = 'human'

    def load_associations(self):
        self.retrieve_associations(ont=self.ont, group=self.group)

    def load_gene_set(self):
        for gene in self.input_object['input']:
            mg = MyGeneInfo()
            gene_curie = ''
            sim_input_curie = ''
            symbol = ''
            if 'MGI' in gene['hit_id']:
                gene_curie =  gene['hit_id']
                sim_input_curie = gene['hit_id'].replace('MGI', 'MGI:MGI')
                symbol = None
            if 'HGNC' in gene['hit_id']:
                gene_curie = gene['hit_id'].replace('HGNC', 'hgnc')
                scope = 'HGNC'
                mg_hit = mg.query(gene_curie,
                                  scopes=scope,
                                  species=self.input_object['parameters']['taxon'],
                                  fields='uniprot, symbol, HGNC',
                                  entrezonly=True)
                try:
                    gene_curie = gene['hit_id']
                    sim_input_curie = 'UniProtKB:{}'.format(mg_hit['hits'][0]['uniprot']['Swiss-Prot'])
                except Exception as e:
                    print(gene, e)

            self.gene_set.append({
                'input_id': gene_curie,
                'sim_input_curie': sim_input_curie,
                'input_symbol': gene['hit_symbol']
            })

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

    def symbol2hgnc(self, symbol):
        mg_hit = self.mg.query('symbol:{}'.format(symbol),
                          fields='HGNC,symbol,taxon',
                          species='human',
                          entrezonly=True)
        if mg_hit['total'] == 1:
            return 'HGNC:{}'.format(mg_hit['hits'][0]['HGNC'])


# Mod1B1_phenotype_similarity
class PhenotypeSimilarity(GenericSimilarity):
    def __init__(self):
        GenericSimilarity.__init__(self)
        self.gene_set = []
        self.input_object = ''
        self.group = ''
        self.ont = ''
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

    def metadata(self):
        print("""Mod1B1 Phenotype Similarity metadata:""")
        pprint(self.meta)

    def load_input_object(self, input_object):
        self.input_object = input_object
        if self.input_object['parameters']['taxon'] == 'mouse':
            self.group = 'mouse'
            self.ont = 'mp'
        if self.input_object['parameters']['taxon'] == 'human':
            self.group = 'human'
            self.ont = 'hp'

    def load_associations(self):
        self.retrieve_associations(ont=self.ont, group=self.group)

    def load_gene_set(self):
        for gene in self.input_object['input']:
            mg = MyGeneInfo()
            gene_curie = ''
            sim_input_curie = ''
            symbol = ''
            if 'MGI' in gene['hit_id']:
                gene_curie = gene['hit_id']
                sim_input_curie = gene['hit_id']
                # if self.ont == 'go':
                #     sim_input_curie = gene.replace('MGI', 'MGI:MGI')
                # else:
                #
                symbol = None
            if 'HGNC' in gene['hit_id']:
                mgi_gene_curie = gene['hit_id'].replace('HGNC', 'hgnc')
                scope = 'HGNC'
                mg_hit = mg.query(mgi_gene_curie,
                                  scopes=scope,
                                  species=self.input_object['parameters']['taxon'],
                                  fields='uniprot, symbol, HGNC',
                                  entrezonly=True)
                try:
                    gene_curie = gene['hit_id']
                    sim_input_curie = gene['hit_id']
                    symbol = mg_hit['hits'][0]['symbol']

                except Exception as e:
                    print(gene, e)
            self.gene_set.append({
                'input_id': gene_curie,
                'sim_input_curie': sim_input_curie,
                'input_symbol': gene['hit_symbol']
            })

    def compute_similarity(self):
        lower_bound = float(self.input_object['parameters']['threshold'])
        results = self.compute_jaccard(self.gene_set, lower_bound)
        for result in results:
            for gene in self.gene_set:
                if gene['sim_input_curie'] == result['input_id']:
                    result['input_symbol'] = gene['input_symbol']
        return results


# Mod1E_interactions
class GeneInteractions(object):
    def __init__(self):
        self.blw = BioLinkWrapper()
        self.gene_set = []
        self.input_object = ''
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
            'predicate': ['blm:interacts with']
        }
        print("""Mod1E Interaction Network metadata:""")
        pprint(self.meta)

    def load_input_object(self, input_object):
        self.input_object = input_object

    def load_gene_set(self):
        for gene in self.input_object['input']:
            self.gene_set.append({
                'input_id': gene['hit_id'],
                'sim_input_curie': gene['hit_id'],
                'input_symbol': gene['hit_symbol']
            })

    def get_interactions(self):
        results = []
        for gene in self.gene_set:
            interactions = self.blw.gene_interactions(gene_curie=gene['sim_input_curie'])
            for assoc in interactions['associations']:
                interaction = self.blw.parse_association(input_id=gene['sim_input_curie'],
                                                          input_label=gene['input_symbol'],
                                                          association=assoc)
                results.append({
                    'input_id': interaction['input_id'],
                    'input_symbol': interaction['input_symbol'],
                    'hit_symbol': interaction['hit_symbol'],
                    'hit_id': interaction['hit_id'],
                    'score': 0,
                })
        return results

# StandardOutput
class StandardOutput(object):
    edge_types = {
        'Mod0': 'pathogenic_for',
        'Mod1A': 'functially_similar_to',
        'Mod1B': 'phenotypically_similar_to',
        'Mod1E': 'interacts_with'
    }
    essence_map ={
        'Mod0': 'disease, gene',
        'Mod1A': 'gene, functional similarity',
        'Mod1B': 'gene, phenotypic similarity',
        'Mod1E': 'protein, interactions'
    }

    def __init__(self, results, input_object):
        self.results = results
        self.input_object = input_object
        self.results_count = len(results)
        self.output_object = self.mod_level_output()
        self.generate_result()

    def mod_level_output(self):
        return {
            'context': 'https://raw.githubusercontent.com/biolink/biolink-model/master/context.jsonld',
            'datetime': str(datetime.now()),
            'id': '',
            'message': '{} results found'.format(self.results_count),
            'n_results': self.results_count,
            'original_question_text': 'What genes are functionally similar to genes associated with {}'.format(
                self.input_object['id']),
            'query_type_id': 'query_id',
            'reasoner_id': 'Orange',
            'response_code': 'OK',
            'restated_question_text': 'What genes are functionally similar to genes associated with {}'.format(
                self.input_object['id']),
            'result_list': [],
            'schema_version': '0.8.0',
            'table_column_names': ['input_id', 'input_symbol', 'result_id', 'result_symbol', 'score'],
            'terms': {'disease': 'gene_id'},
            'tool_version': 'orange',
            'type': 'medical_translator_query_response'
        }

    def generate_result(self):
        for result in self.results:
            result_meta = {'confidence': result['score'],
                           'essence': StandardOutput.essence_map[result['module']],
                           'id': result['module'],
                           'reasoner_id': "orange",
                           'result_graph': {
                               'edge_list': [],
                               'node_list': [],
                           },
                           'result_type': 'gene',
                           'row_data': [",".join(list(result.keys()))],
                           'text': ''}

            edge = {'is_defined_by': 'orange',
                    'provided_by': 'BioLink',
                    'source_id': result['input_id'],
                    'target_id': result['hit_id'],
                    'type': StandardOutput.edge_types[result['module']]
                    }

            nodes = [{
                'description': 'gene',
                'id': result['hit_id'],
                'name': result['hit_symbol'],
                'type': 'gene',
                'uri': ''},
                {
                    'description': 'gene',
                    'id': result['input_id'],
                    'name': result['input_symbol'],
                    'type': 'gene',
                    'uri': ''
                },
            ]

            result_meta['result_graph']['edge_list'].append(edge)
            for node in nodes:
                result_meta['result_graph']['node_list'].append(node)
            self.output_object['result_list'].append(result_meta)
