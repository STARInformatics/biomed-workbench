import workflow
import workflow_async
import cProfile

testData = {
	"id" : "MONDO:0005148"
}

testSet = {
	"profile": False,
	"print": True,
	"async": False
}

geneSet = [{'hit_id': 'HGNC:10778', 'hit_symbol': 'SFRP4', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:11006', 'hit_symbol': 'SLC2A2', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:11009', 'hit_symbol': 'SLC2A4', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:11132', 'hit_symbol': 'SNAP25', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:11621', 'hit_symbol': 'HNF1A', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:11630', 'hit_symbol': 'HNF1B', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:11766', 'hit_symbol': 'TGFB1', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:11892', 'hit_symbol': 'TNF', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:11917', 'hit_symbol': 'TNFRSF1B', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:12711', 'hit_symbol': 'VPS26A', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:12762', 'hit_symbol': 'WFS1', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:1318', 'hit_symbol': 'C3', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:14163', 'hit_symbol': 'FAM234A', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:14335', 'hit_symbol': 'PLEKHA1', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:14464', 'hit_symbol': 'KCNK16', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:1477', 'hit_symbol': 'CAPN10', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:1504', 'hit_symbol': 'CASP3', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:1509', 'hit_symbol': 'CASP8', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:18259', 'hit_symbol': 'ITLN1', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:19165', 'hit_symbol': 'TBC1D4', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:19217', 'hit_symbol': 'THADA', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:20303', 'hit_symbol': 'SLC30A8', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:21050', 'hit_symbol': 'CDKAL1', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:22984', 'hit_symbol': 'JADE2', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:24212', 'hit_symbol': 'CISD2', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:24319', 'hit_symbol': 'CMIP', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:24678', 'hit_symbol': 'FTO', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:25257', 'hit_symbol': 'TMEM18', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:2596', 'hit_symbol': 'CYP1A2', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:26418', 'hit_symbol': 'TMEM155', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:28510', 'hit_symbol': 'GLIS3', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:29913', 'hit_symbol': 'ZC3HC1', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:31498', 'hit_symbol': 'MIR10B', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:31578', 'hit_symbol': 'MIR200A', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:31581', 'hit_symbol': 'MIR203A', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:31601', 'hit_symbol': 'MIR221', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:31613', 'hit_symbol': 'MIR27A', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:31649', 'hit_symbol': 'MIR98', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:3176', 'hit_symbol': 'EDN1', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:31773', 'hit_symbol': 'MIR335', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:31868', 'hit_symbol': 'MIR375', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:32055', 'hit_symbol': 'MIR409', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:32067', 'hit_symbol': 'MIR485', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:32533', 'hit_symbol': 'MIR487B', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:32791', 'hit_symbol': 'MIR33B', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:3356', 'hit_symbol': 'ENPP1', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:33627', 'hit_symbol': 'C2CD4A', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:33628', 'hit_symbol': 'C2CD4B', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:33658', 'hit_symbol': 'MIR744', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:33682', 'hit_symbol': 'MIR939', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:35325', 'hit_symbol': 'MIR1260A', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:35371', 'hit_symbol': 'MIR1306', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:35372', 'hit_symbol': 'MIR1307', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:35392', 'hit_symbol': 'MIR1908', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:37310', 'hit_symbol': 'MIR2116', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:38174', 'hit_symbol': 'MIR3173', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:392', 'hit_symbol': 'AKT2', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:4191', 'hit_symbol': 'GCG', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:4195', 'hit_symbol': 'GCK', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:4196', 'hit_symbol': 'GCKR', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:4456', 'hit_symbol': 'GPD2', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:4632', 'hit_symbol': 'GSTM1', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:4901', 'hit_symbol': 'HHEX', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:4922', 'hit_symbol': 'HK1', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:50004', 'hit_symbol': 'MIR6741', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:5001', 'hit_symbol': 'HMG20A', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:50077', 'hit_symbol': 'MIR8061', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:5010', 'hit_symbol': 'HMGA1', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:5024', 'hit_symbol': 'HNF4A', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:5329', 'hit_symbol': 'IAPP', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:5344', 'hit_symbol': 'ICAM1', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:5360', 'hit_symbol': 'ID1', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:571', 'hit_symbol': 'AP3S2', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:59', 'hit_symbol': 'ABCC8', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:6018', 'hit_symbol': 'IL6', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:6257', 'hit_symbol': 'KCNJ11', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:6294', 'hit_symbol': 'KCNQ1', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:6344', 'hit_symbol': 'KL', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:6554', 'hit_symbol': 'LEPR', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:6882', 'hit_symbol': 'MAPK8IP1', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:7227', 'hit_symbol': 'MRAS', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:7464', 'hit_symbol': 'MTNR1B', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:7762', 'hit_symbol': 'NEUROD1', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:7839', 'hit_symbol': 'NKX6-1', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:785', 'hit_symbol': 'ATF3', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:7873', 'hit_symbol': 'NOS2', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:7876', 'hit_symbol': 'NOS3', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:7882', 'hit_symbol': 'NOTCH2', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:812', 'hit_symbol': 'ATP2A2', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:8618', 'hit_symbol': 'PAX4', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:8744', 'hit_symbol': 'PCSK2', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:8840', 'hit_symbol': 'PEPD', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:9236', 'hit_symbol': 'PPARG', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:9291', 'hit_symbol': 'PPP1R3A', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:9395', 'hit_symbol': 'PRKCB', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:9833', 'hit_symbol': 'MOK', 'input_id': 'MONDO:0005148'}, {'hit_id': 'HGNC:994', 'hit_symbol': 'BCL2L11', 'input_id': 'MONDO:0005148'}, {'hit_id': 'MGI:1855937', 'hit_symbol': 'Gm14226', 'input_id': 'MONDO:0005148'}, {'hit_id': 'RGD:628626', 'hit_symbol': 'Cyp3a23/3a1', 'input_id': 'MONDO:0005148'}, {'hit_id': 'RGD:708379', 'hit_symbol': 'Cyp3a2', 'input_id': 'MONDO:0005148'}]


# Execute workflow for benchmarking
def workflow2_sync(testData):
	"""
	:param bioLinkWrapper:
	:return: candidates

	# execute the following functions in a chain
	# profile the execution with cTime

	'/api/disease/diabetes mellitus',

	# these all take the same input?
	'/api/workflow/mod0/MONDO:0005148',
	'/api/workflow/mod1a/MONDO:0005148',
	'/api/workflow/mod1e/MONDO:0005148',
	'/api/workflow/mod1b1/MONDO:0005148',

	'/api/gene-to-pathway/HGNC:406',
	'/api/data/HGNC:406',
	'/api/pathway-to-sbgn/R-HSA-389661',
	'/api/pathway-to-png/R-HSA-389661',
	'/api/get-ncats-data/MONDO:0005148'

	"""


	# print("mod0")
	# data0 = workflow.mod0_disease_lookup(testData["id"])
	# if testSet["profile"]:
	# 	cProfile.run('workflow.mod0_disease_lookup(testData["id"])')
	# if testSet["print"]:
	# 	print(data0)

	"""
	print("mod1a")
	data1a = workflow.mod1a_functional_similarity(data0)
	if testSet["profile"]:
		cProfile.run('workflow.mod1a_functional_similarity(data0)')
	if testSet["print"]:
		print(data1a)

	"""

	"""
	print("mod1b1")
	data1b = workflow.mod1b1_phenotype_similarity(geneSet)
	if testSet["profile"]:
		cProfile.run('workflow.mod1b1_phenotype_similarity(geneSet)')
	if testSet["print"]:
		print(data1b)
	"""

	print("mod1e")
	data1e = workflow.mod1e_gene_interactions(geneSet)
	if testSet["profile"]:
		cProfile.run('workflow.mod1e_gene_interactions(geneSet)')
	if testSet["print"]:
		print(data1e)

	results = {
		#"mod0": data0,
		#"mod1a": data1a,
		#"mod1b": data1b,
		"mod1e": data1e
	}

	return results

def workflow2_async(testData):

	print("mod0")
	print("async TODO")
	data0 = workflow_async.mod0_disease_lookup(testData["id"])
	if testSet["profile"]:
		cProfile.run('workflow_async.mod0_disease_lookup(testData["id"])')
	if testSet["print"]:
		print(data0)

	"""
	print("mod1a")
	data1a = workflow.mod1a_functional_similarity(data0)
	if testSet["profile"]:
		cProfile.run('workflow_async.mod1a_functional_similarity(data0)')
	if testSet["print"]:
		print(data1a)

	"""
	print("mod1b1")
	print("async TODO")
	data1b = workflow_async.mod1b1_phenotype_similarity(geneSet)
	if testSet["profile"]:
		cProfile.run('workflow_async.mod1b1_phenotype_similarity(geneSet)')
	if testSet["print"]:
		print(data1b)


	print("mod1e")
	print("async TODO")
	data1e = workflow_async.mod1e_gene_interactions(geneSet)
	if testSet["profile"]:
		cProfile.run('workflow_async.mod1e_gene_interactions(geneSet)')
	if testSet["print"]:
		print(data1e)


	results = {
		"mod0": data0,
		#"mod1a": data1a,
		"mod1b": data1b,
		"mod1e": data1e
	}

	return results

if testSet["async"]:
	workflow2_async(testData)
else:
	workflow2_sync(testData)
