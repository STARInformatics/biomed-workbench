from cachetools import cached, LRUCache
from threading import RLock

from .biolink_client import BioLinkWrapper
import pandas as pd
from os import makedirs
from html3.html3 import XHTML

from .Mod0_lookups import LookUp
from .Mod1A_functional_sim import FunctionalSimilarity
from .Mod1B1_phenotype_similarity import PhenotypeSimilarity
from .Mod1E_interactions import GeneInteractions

@cached(cache=LRUCache(maxsize=32), lock=RLock())
def mod0_disease_lookup(mondo_id):
    lu = LookUp()
    input_object = {
        'input': mondo_id,
        'parameters': {
            'taxon': 'human',
            'threshold': None,
        },
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

def load_genes(model, data, threshold):
    # Module specification
    inputParameters = {
        'input': data,
        'parameters': {
            'taxon': 'human',
            'threshold': threshold,
        },
    }
    # Load the computation parameters
    model.load_input_object(inputParameters)
    model.load_gene_set()

def similarity(model, data, threshold=0.75):
    load_genes(model, data, threshold)
    model.load_associations()

    # Perform the comparison
    results = model.compute_similarity()
    return results

def mod1a_functional_similarity(data, threshold=0.75):
    results = similarity(
        FunctionalSimilarity(),
        data,
        threshold,
    )
    return results

def mod1b1_phenotype_similarity(data, threshold=0.50):
    results = similarity(
        PhenotypeSimilarity(),
        data,
        threshold,
    )
    return results

def mod1e_gene_interactions(data):
    model = GeneInteractions()
    load_genes(model, data, None)
    results = model.get_interactions()
    results_table = pd.DataFrame(results)
    counts = results_table['hit_symbol'].value_counts().rename_axis('unique_values').to_frame('counts').reset_index()
    high_counts = counts[counts['counts'] > 12]['unique_values'].tolist()
    final_results_table = pd.DataFrame(results_table[results_table['hit_symbol'].isin(high_counts)])
    return final_results_table.to_dict(orient='records')

def module_runner(data, module_id):
    if module_id == 'mod1a':
        return mod1a_functional_similarity(data)
    elif module_id == 'mod1b1':
        return mod1b1_phenotype_similarity(data)
    elif module_id == 'mod1e':
        return mod1e_gene_interactions(data)
    else:
        raise Exception('Invalid module_id: {}'.format(moudleid))

def run_workflow(mondo_id):
    modules = [
        mod1a_functional_similarity,
        mod1b1_phenotype_similarity,
        mod1e_gene_interactions,
    ]

    cpu_count = mp.cpu_count()
    min_cpu_count = min(cpu_count, len(modules))
    print('Using {}/{} CPUs'.format(min_cpu_count, cpu_count))
    input_object, disease_associated_genes, genes = mod0_disease_lookup(mondo_id)
    # pool = mp.Pool(processes=min_cpu_count)
    with get_context("spawn").Pool() as pool:
        processes = [pool.apply_async(module, args=(genes,)) for module in modules]

        results = []

        for i, p in enumerate(processes):
            print(i)
            results += p.get()
            print(len(results))

    results = sorted(results, key=lambda d: -d.get('score', 0))

    return results

# if __name__ == '__main__':
def run():
    from pprint import pprint
    results = run_workflow('MONDO:0019391')
    pprint(results[:100])
    quit()

    input_object, disease_associated_genes, input_curie_set = mod0_disease_lookup('MONDO:0019391')
    # Mod1A_results = mod1a_jaccard_similarity(input_curie_set)
    # Mod1B_results = mod1b1_phenotype_similarity(input_curie_set)
    Mod1E_results = mod1e_gene_interactions(input_curie_set)

    results = []
    # results = sorted(results, key=lambda d: -d['score'])

    for result in Mod1E_results:
        result['module'] = 'Mod1E'
