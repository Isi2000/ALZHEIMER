import requests
import xml.etree.ElementTree as ET
from tqdm import tqdm
import json
import pandas as pd
import numpy as np
import time

def get_pubmed_ids(term):
    """
    Fetch PubMed IDs for a specific term.

    Args:
        term (str): The search term.
        retstart (int): The index of the first record to retrieve.
        retmax (int, optional): The maximum number of records to retrieve. Default is 50.

    Returns:
        list: List of PubMed IDs.
    """

    mail = "elisa.fabbri40@studio.unibo.it"
    all_ids = []
    esearch_url_before90 = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={term}&mindate=800&maxdate=1990&format=json&email={mail}"
    response_before90 = requests.get(esearch_url_before90)
    retmax_before90 = response_before90.json()["esearchresult"]["count"]
    esearch_url_1_before90 = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={term}&mindate=800&maxdate=1990&retstart={0}&retmax={9998}&format=json&email={mail}"
    response_1_before90 = requests.get(esearch_url_1_before90)
    ids_before90 = response_1_before90.json()["esearchresult"]["idlist"]
    all_ids.extend(ids_before90)
    print(len(ids_before90))
    with open('./DATA/' + 'data_before90.csv', 'w') as file:
            for id in ids_before90:
                file.write(id + ',')
    
    for year in range(1990, 2023):
        filename = f'data_{year}.csv'
        ids_ = []
        for i in tqdm(range(11)):
            time.sleep(2)
            min_month = i + 1
            max_month = i + 2
            min_date = f"{year}/{min_month:02d}/01"
            if max_month < 13:
                max_date = f"{year}/{max_month:02d}/01"
            else:
                max_date = f"{year+1}/01/01"
                
            esearch_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={term}&mindate={min_date}&maxdate={max_date}&format=json&email={mail}"
            response = requests.get(esearch_url)
            retmax = response.json()["esearchresult"]["count"]
            time.sleep(1)
            esearch_url_1 = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={term}&mindate={min_date}&maxdate={max_date}&retstart={0}&retmax={retmax}&format=json&email={mail}"
            response_1 = requests.get(esearch_url_1)
            ids = np.array(response_1.json()["esearchresult"]["idlist"])
            ids_.extend(ids)
            with open('./DATA/' + filename, 'w') as file:
                for id in ids_:
                    file.write(id + ',')
                    
    
    return all_ids

ids = get_pubmed_ids("alzheimer's disease")
with open('./UNIQUE_IDS.csv', 'w') as file:
                for id in ids:
                    file.write(id + ',')
