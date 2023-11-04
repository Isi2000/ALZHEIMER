import requests
import xml.etree.ElementTree as ET
from tqdm import tqdm
import json

def get_pubmed_ids(term, retstart, retmax=50):
    all_ids = []
    esearch_url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={term}&retstart={retstart}&retmax={retmax}&format=json&sort=relevance'
    response = requests.get(esearch_url)
    ids = response.json()['esearchresult']['idlist']
    all_ids.extend(ids)

    return all_ids

def fetch_pubmed_entries(ids):
    id_string = ','.join(ids)
    efetch_url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={id_string}&rettype=abstract'
    response = requests.get(efetch_url)
    return response.text


def extract_data_from_efetch(xml_content):
    root = ET.fromstring(xml_content)
    articles_data = []

    for article in root.findall(".//PubmedArticle"):
        # Extract publication date
        pub_date_elem = article.find(".//PubDate")
        year = pub_date_elem.findtext(".//Year") or 'Unknown'
        month = pub_date_elem.findtext(".//Month") or 'Unknown'
        day = pub_date_elem.findtext(".//Day") or 'Unknown'
        pub_date = f"{year}-{month}-{day}"

        # Extract authors
        authors_elem = article.find(".//AuthorList")
        if authors_elem is not None:
            authors = [f"{author.findtext('.//LastName') or 'Unknown'} {author.findtext('.//ForeName') or 'Unknown'}" for author in authors_elem.findall(".//Author")]
        else:
            authors = ['Unknown']

        # Extract keywords
        keyword_elems = article.findall(".//KeywordList/Keyword")
        article_keywords = [keyword.text for keyword in keyword_elems]

        #Extract ID
        pmid_elem = article.find('.//PMID[@Version="1"]')
        if pmid_elem is not None:
            pmid = pmid_elem.text
        else:
            pmid = None
        # Extract cited articles ids
        # NOTA: PUOI ESTRARRE ANCHE TITOLI E AUTORI SE SERVE
        cited_elem = article.findall(".//ReferenceList/Reference")
        cited_arts = [reference.find('.//ArticleIdList/ArticleId[@IdType="pubmed"]').text if reference.find('.//ArticleIdList/ArticleId[@IdType="pubmed"]') is not None else None for reference in cited_elem]

                
        article_data = {
            'Id' : pmid,
            'Authors': authors,
            'Date' : pub_date,
            'Keywords': article_keywords,
            'cited_arts': cited_arts,
        }

        articles_data.append(article_data)

    return articles_data

# Usage
for i in tqdm(range(199)):
    ids = get_pubmed_ids('alzheimer', retstart=i)
    fetched = fetch_pubmed_entries(ids)
    articles_data = extract_data_from_efetch(fetched)

    # Save data to a JSON file
    with open(f'./DATA/rel_data_{i}.json', 'w') as json_file:
        json.dump(articles_data, json_file)

