from ontobio.ontol_factory import OntologyFactory
from ontobio.io.gafparser import GafParser
from ontobio.assoc_factory import AssociationSetFactory
from typing import List
from ontobio.analysis.semsim import jaccard_similarity
from .gene_set import GeneSetWrapper
from collections import namedtuple

class GenericSimilarity(GeneSetWrapper):

    def __init__(self, taxon='human', threshold=0.0) -> None:
        GeneSetWrapper.__init__(self, taxon)

        # parameterized fields
        self.taxon = taxon
        self.threshold = threshold

        # internal fields
        self._associations = []
        self._ontology = ''
        self._assocs = ''
        self._afactory = AssociationSetFactory()

        # named data schema for a similarity object
        # self.SimiliarityScore = namedtuple('SimiliarityScore', ('score', 'input_id') + self.AnnotatedGene._fields)

    def load_associations(self, taxon):
        taxon_map = {
            'human': 'NCBITaxon:9606',
            'mouse': 'NCBITaxon:10090',
        }

        ofactory = OntologyFactory()
        self._ontology = ofactory.create(self.ont)
        p = GafParser()
        url = ''
        if self.ont == 'go':
            go_roots = set(self._ontology.descendants('GO:0008150') + self._ontology.descendants('GO:0003674'))
            sub_ont = self._ontology.subontology(go_roots)
            if taxon == 'mouse':
                url = "http://current.geneontology.org/annotations/mgi.gaf.gz"
            if taxon == 'human':
                url = "http://current.geneontology.org/annotations/goa_human.gaf.gz"
            assocs = p.parse(url)
            self._assocs = assocs
            assocs = [x for x in assocs if 'header' not in x.keys()]
            assocs = [x for x in assocs if x['object']['id'] in go_roots]
            self._associations = self._afactory.create_from_assocs(assocs, ontology=sub_ont)
        else:
            self._associations = \
                self._afactory.create(
                        ontology=self._ontology,
                        subject_category='gene',
                        object_category='phenotype',
                        taxon=taxon_map[taxon]
            )

    def _trim_mgi_prefix(self, input_gene, subject_curie):

        if input_gene is not None and 'MGI:MGI:' not in subject_curie and 'MGI:MGI:' in input_gene:
            return input_gene[len('MGI:'):]
        else:
            return input_gene

    def compute_similarity(self, gene_set, threshold=None):
        annotated_gene_set = self.load_gene_set(gene_set)

        if threshold is None:
            threshold = self.threshold

        results = self.compute_jaccard(annotated_gene_set, threshold)

        for result in results:
            print(result)
            if self.taxon == 'human':
                result['hit_id'] = self.symbol2hgnc(result['hit_symbol'])
            for gene in annotated_gene_set:
                if gene['sim_input_curie'] != result['input_id']:
                    result['input_id'] = self.symbol2hgnc(result['input_symbol'])

        return results


    def compute_jaccard(self, input_genes, threshold) -> List[dict]:

        similarGenes = []
        for index, annotated_gene in enumerate(input_genes):
            for subject_id in self._associations.subject_label_map.keys():

                input_gene_id = self._trim_mgi_prefix(input_gene=annotated_gene["sim_input_curie"], subject_curie=subject_id)
                if input_gene_id is not subject_id:
                    score = jaccard_similarity(self._associations, input_gene_id, subject_id)

                    if float(score) > float(threshold):
                        subject_label = self._associations.label(subject_id)

                        # TODO: This can be seen as an extension of an existing datatype
                        # ... and would be more rigorously constructed given a term system, or prototypical inheritance
                        similarGenes.append(
                            {
                                'input_id': input_gene_id,
                                'input_symbol': annotated_gene['gene_symbol'],

                                'hit_symbol': subject_label,
                                'hit_id': subject_id,

                                'score': score,
                            }
                        )

        return similarGenes
