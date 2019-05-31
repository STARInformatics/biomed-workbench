from cachetools import cached, LRUCache
from threading import RLock

from BioLink.biolink_client import BioLinkWrapper
import pandas as pd
from os import makedirs
from html3.html3 import XHTML

from .Mod0_disease_gene_lookup import LookUp
from .Mod1A_functional_sim import FunctionalSimilarity
from .Mod1B1_phenotype_similarity import PhenotypeSimilarity
from .Mod1E_interactions import GeneInteractions

from collections import namedtuple

# these structs are too small to be a class, but too common not to schematize throughout the application
SimilarityModel = namedtuple('SimilarityModel', ['taxon', 'threshold'])

def remove_duplicates(results:list) -> list:
    """
    Ensures that the hit_id in each result is unique
    """
    hits = set()
    l = []
    for d in results:
        hit_id = d.get('hit_id')
        if hit_id not in hits:
            hits.add(hit_id)
            l.append(d)
    return l

@cached(cache=LRUCache(maxsize=32), lock=RLock())
def mod0_disease_gene_lookup(mondo_id, threshold=0.0):
    lu = LookUp()
    input_object = {
        'input': mondo_id,
        'parameters': SimilarityModel('human', threshold)
    }

    lu.load_input_object(input_object=input_object)
    # get genes associated with disease from Biolink
    disease_associated_genes = lu.disease_geneset_lookup()
    # create list of gene curies for downstream module input
    input_curie_set = disease_associated_genes[['hit_id', 'hit_symbol']].to_dict(orient='records')
    # show the disease associated genes
    disease_associated_genes['modules'] = 'Mod0'
    for d in input_curie_set:
        d['input_id'] = mondo_id
    return input_curie_set

def mod1a_functional_similarity(geneSet, threshold=0.0, duplicates=False):
    results = FunctionalSimilarity('human', threshold).compute_similarity(geneSet)
    if not duplicates:
        return remove_duplicates(results)
    else:
        return results

def mod1b1_phenotype_similarity(geneSet, threshold=0.0, duplicates=False):
    results = PhenotypeSimilarity('human', threshold).compute_similarity(geneSet)
    if not duplicates:
        return remove_duplicates(results)
    else:
        return results

def mod1e_gene_interactions(data, duplicates=False):
    model = GeneInteractions()
    load_genes(model, data, None)
    results = model.get_interactions()
    results_table = pd.DataFrame(results)
    counts = results_table['hit_symbol'].value_counts().rename_axis('unique_values').to_frame('counts').reset_index()
    high_counts = counts[counts['counts'] > 12]['unique_values'].tolist()
    final_results_table = pd.DataFrame(results_table[results_table['hit_symbol'].isin(high_counts)])
    results = final_results_table.to_dict(orient='records')
    if not duplicates:
        return remove_duplicates(results)
    else:
        return results

if __name__ == '__main__':
    from pprint import pprint
    input_object, disease_associated_genes, input_curie_set = mod0_disease_gene_lookup('MONDO:0019391')
    # Mod1A_results = mod1a_jaccard_similarity(input_curie_set)
    # Mod1B_results = mod1b1_phenotype_similarity(input_curie_set)
    Mod1E_results = mod1e_gene_interactions(input_curie_set)

    results = []
    # results = sorted(results, key=lambda d: -d['score'])

    for result in Mod1E_results:
        result['module'] = 'Mod1E'
