import os
import click
import requests
import shutil

import pandas as pd

COMPLEX = 'ComplexParticipantsPubMedIdentifiers_human.txt'
PE = 'NCBI2Reactome_PE_All_Levels.txt'
REACTIONS = 'NCBI2ReactomeReactions.txt'
CHEMICALS = 'ChEBI2Reactome_PE_Reactions.txt'

PREFIX = 'ncbigene'

def download(url:str, download_dir:str='') -> str:
    _, filename = url.rsplit('/', 1)
    path = os.path.join(download_dir, filename)
    with requests.get(url, stream=True) as r:
        with open(path, 'wb+') as f:
            for chunk in r.iter_content(chunk_size=128):
                f.write(chunk)
    return path

def download_files(download_dir, force_download=False):
    filenames = [COMPLEX, PE, REACTIONS, CHEMICALS]
    for filename in filenames:
        if os.path.exists(os.path.join(download_dir, filename)) and not force_download:
            continue
        url = 'https://reactome.org/download/current/' + filename
        path = download(url, download_dir)
        print('Downloaded {}'.format(path))

@click.command()
@click.option('--download-dir', '-d', default='backend/data')
@click.option('--force-download', '-f', is_flag=True)
@click.option('--output', '-o', default='backend/data/id_mapping.csv')
def main(download_dir, force_download, output):
    """
    Builds up a CSV correlating labels from the Reactome SBGN's with identifiers

    Use: `python scripts/build_id_mapping_csv.py`
    """
    download_files(download_dir, force_download)

    path = os.path.join(download_dir, PE)
    print('Parsing {}'.format(path))
    df = pd.read_csv(path, header=None, dtype=str, sep='\t')
    df['name'] = df[2].apply(lambda x: x.split('[', 1)[0].strip())
    df['id'] = df[0].apply(lambda x: '{}:{}'.format(PREFIX, x))
    df['species'] = df[7]

    df_genes = df[df['species'] == 'Homo sapiens'][['id', 'name']]

    path = os.path.join(download_dir, REACTIONS)
    print('Parsing {}'.format(path))
    df = pd.read_csv(path, header=None, dtype=str, sep='\t')
    df['name'] = df[3]
    df['id'] = df[1]
    df['species'] = df[5]

    df_reactions = df[df['species'] == 'Homo sapiens'][['id', 'name']]

    path = os.path.join(download_dir, COMPLEX)
    print('Parsing {}'.format(path))
    df = pd.read_csv(path, dtype=str, sep='\t')
    df['name'] = df['name'].apply(lambda x: x.split('[', 1)[0].strip())
    df['id'] = df['identifier']

    df_complex = df[['id', 'name']]

    path = os.path.join(download_dir, CHEMICALS)
    print('Parsing {}'.format(path))
    df = pd.read_csv(path, header=None, dtype=str, sep='\t')
    df['name'] = df[2].apply(lambda x: x.split('[', 1)[0].strip())
    df['id'] = df[0]

    df_chemical = df[['id', 'name']]

    df = pd.concat([df_complex, df_genes, df_reactions, df_chemical])

    df = df.drop_duplicates()

    if not output.endswith('.csv'):
        output += '.csv'

    print('Saving to {}'.format(output))

    df.to_csv(output, sep='\t', index=False)

if __name__ == '__main__':
    main()
