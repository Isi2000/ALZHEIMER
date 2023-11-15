import requests
import xml.etree.ElementTree as ET
import json
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import time
import numpy as np


def split_ids(id_list, cluster_size=10):
    return [id_list[i:i + cluster_size] for i in range(0, len(id_list), cluster_size)]

def read_ids_from_csv(file_path):
    """
    Read PubMed IDs from a CSV file.

    Args:
        file_path (str): Path to the CSV file containing PubMed IDs.

    Returns:
        list: List of PubMed IDs.
    """
    column_label = 'PubMed_ID'  
    df = pd.read_csv(file_path, names=[column_label], header=0)
    return df[column_label].tolist()  # Adjust 'PubMed_ID' based on your CSV column name

def parse_article(article):
    """
    Parse individual PubMed article data from XML.

    Args:
        article (xml.etree.ElementTree.Element): XML element for a single article.

    Returns:
        dict: Parsed article data.
    """
    # Extract PubMed ID
    pubmed_id = article.find(".//MedlineCitation/PMID").text

    # Extract publication date
    pub_date_elem = article.find(".//PubDate")
    year = pub_date_elem.findtext(".//Year") or "Unknown"
    month = pub_date_elem.findtext(".//Month") or "Unknown"
    day = pub_date_elem.findtext(".//Day") or "Unknown"
    pub_date = f"{year}-{month}-{day}"

    # Extract authors
    authors_elem = article.find(".//AuthorList")
    authors = [
        f"{author.findtext('.//LastName') or author.findtext('.//CollectiveName') or 'pd'} {author.findtext('.//ForeName') or author.findtext('.//CollectiveName') or 'pd'}"
        for author in authors_elem.findall(".//Author")
    ] if authors_elem is not None else ["Unknown"]

    # Extract MeSH terms with MajorTopicYN distinction
    mesh_elems = article.findall(".//MeshHeadingList/MeshHeading")
    mesh_terms = []
    for mesh in mesh_elems:
        descriptor = mesh.find('.//DescriptorName')
        descriptor_name = descriptor.text
        descriptor_major_topic = descriptor.get('MajorTopicYN') == 'Y'

        # Process QualifierNames if any
        qualifiers = mesh.findall('.//QualifierName')
        for qual in qualifiers:
            qual_name = qual.text
            qual_major_topic = qual.get('MajorTopicYN') == 'Y'
            mesh_terms.append({
                'DescriptorName': descriptor_name,
                'DescriptorMajorTopic': descriptor_major_topic,
                'QualifierName': qual_name,
                'QualifierMajorTopic': qual_major_topic
            })

        # Include DescriptorName if there are no QualifierNames
        if not qualifiers:
            mesh_terms.append({
                'DescriptorName': descriptor_name,
                'DescriptorMajorTopic': descriptor_major_topic,
                'QualifierName': None,
                'QualifierMajorTopic': None
            })

    return {
        "Id": pubmed_id,
        "Dates": pub_date,
        "Authors": authors,
        "MeSH_Terms": mesh_terms
    }

porcodio = []
def fetch_data_for_ids(ids, retries=5, delay=2):
    for attempt in range(retries):
        id_string = ",".join(str(id) for id in ids)
        efetch_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={id_string}&rettype=abstract"
        
        response = requests.get(efetch_url)

        if response.status_code == 200:
            try:
                root = ET.fromstring(response.text)
                return [parse_article(article) for article in root.findall(".//PubmedArticle")]
            except ET.ParseError as e:
                print(f"Error parsing XML for IDs: {ids}")
                print(f"Error details: {e}")
                break
            except Exception as e:
                print(f"An unexpected error occurred for IDs: {ids}")
                print(f"Error details: {e}")    
                break
            time.sleep(delay)
        else:
            print(f"Failed to fetch data for IDs: {ids}. Status Code: {response.status_code}")
            print(f"Failed XML:\n{response.text}")
            time.sleep(delay)
            porcodio.append(ids)
            #np.savetxt(f"./DATA/{ids[0]}.csv", ids, delimiter=",", fmt='%s')
            break

    return []

def fetch_pubmed(ids_list):
    """
    Fetch PubMed data sequentially for multiple lists of IDs.

    Args:
        ids_list (list of list): List containing sublists of PubMed IDs.

    Returns:
        pd.DataFrame: DataFrame containing combined PubMed data.
    """
    all_results = []

    for ids in tqdm(ids_list):
        fetched_data = fetch_data_for_ids(ids)
        all_results.extend(fetched_data)

    return pd.DataFrame(all_results)

# Usage
file_path = 'ids.csv'  
ids = read_ids_from_csv(file_path)
splitted_ids = split_ids(ids)
num_b = 0
splitted_ids = [splitted_ids[i:i+200] for i in range(num_b, len(splitted_ids),200)]
print(len(splitted_ids))
for batch_num, ids in enumerate(splitted_ids):
    df = fetch_pubmed(ids)
    df.to_json(f"./AUITOOOO/pubmed_data_{num_b+batch_num}_nuovi.json", orient="records", lines=True)
    #print(df)
    
#df = fetch_pubmed(splitted_ids)
#df.to_json("pubmed_data.json", orient="records", lines=True)
np.savetxt("./DATA1/dati_non_riusciti_nuovi.csv", porcodio, delimiter=",", fmt='%s')

