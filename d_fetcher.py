import requests
import xml.etree.ElementTree as ET
from tqdm import tqdm
import json
import pandas as pd

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
    all_ids = []
    for year in range(2015, 2016):
        for i in tqdm(range(6)):
            min_month = i * 2 + 1
            max_month = i * 2 + 2
            if max_month > 12:
                max_month = 12
            min_date = f"{year}/{min_month:02d}"
            max_date = f"{year}/{max_month:02d}"

            
            esearch_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={term}&mindate={min_date}&maxdate={max_date}&format=json"
            response = requests.get(esearch_url)
            retmax = response.json()["esearchresult"]["count"]
            esearch_url_1 = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={term}&mindate={min_date}&maxdate={max_date}&retstart={0}&retmax={retmax}&format=json"
            response_1 = requests.get(esearch_url_1)
            ids = response_1.json()["esearchresult"]["idlist"]
            all_ids.extend(ids)
    print(len(all_ids))
    return all_ids

def split_ids(id_list):
    return [id_list[i:i + 10] for i in range(0, len(id_list), 10)]


def fetch_pubmed(ids):
    """
    Fetch and Link PubMed data for a list of PubMed IDs.

    Args:
        ids (list): List of PubMed IDs.

    Returns:
        pd.DataFrame: DataFrame containing PubMed data.
    """
    id_string = ",".join(ids)
    efetch_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={id_string}&rettype=abstract"
    response = requests.get(efetch_url)
    xml_data = response.text
    root = ET.fromstring(xml_data)
    articles_dates = []
    articles_authors = []
    articles_kwords = []
    for article in root.findall(".//PubmedArticle"):
        # Extract publication date
        pub_date_elem = article.find(".//PubDate")
        year = pub_date_elem.findtext(".//Year") or "Unknown"
        month = pub_date_elem.findtext(".//Month") or "Unknown"
        day = pub_date_elem.findtext(".//Day") or "Unknown"
        pub_date = f"{year}-{month}-{day}"
        articles_dates.append(pub_date)

        # Extract authors
        authors_elem = article.find(".//AuthorList")
        if authors_elem is not None:
            authors = [
                f"{author.findtext('.//LastName') or 'Unknown'} {author.findtext('.//ForeName') or 'Unknown'}"
                for author in authors_elem.findall(".//Author")
            ]
        else:
            authors = ["Unknown"]
        articles_authors.append(authors)

        # Extract keywords
        keyword_elems = article.findall(".//KeywordList/Keyword")
        article_keywords = [keyword.text for keyword in keyword_elems]
        articles_kwords.append(article_keywords)

    articles_cited = []
    articles_cited_in = []
    string_for_smart_linking = ""
    for i in ids:
        string_for_smart_linking += f"&id={i}"
    elink_url = (
        f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&linkname=pubmed_pubmed_refs"
        + string_for_smart_linking
    )
    elink_url_cited_in = (
        f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&linkname=pubmed_pubmed_citedin"
        + string_for_smart_linking
    )

    response_l = requests.get(elink_url)
    xml_data_l = response_l.text

    response_cited_in = requests.get(elink_url_cited_in)
    xml_data_cited_in = response_cited_in.text

    root_l = ET.fromstring(xml_data_l)
    root_cited_in = ET.fromstring(xml_data_cited_in)

    for link in root_l.findall(".//LinkSet"):
        link_elems = link.findall(".//LinkSetDb/Link/Id")
        cited_arts = [art.text for art in link_elems]
        articles_cited.append(cited_arts)

    for link in root_cited_in.findall(".//LinkSet"):
        link_elems = link.findall(".//LinkSetDb/Link/Id")
        cited_arts = [art.text for art in link_elems]
        articles_cited_in.append(cited_arts)
    print(len(ids))
    print(len(articles_dates))
    print(len(articles_authors))
    print(len(articles_kwords))
    print(len(articles_cited))
    print(len(articles_cited_in))

    data = pd.DataFrame(
        {
            "Id": ids,
            "Dates": articles_dates,
            "Authors": articles_authors,
            "Keywords": articles_kwords,
            "Cited_Articles": articles_cited,
            "Articles_Cited_In": articles_cited_in,
        }
    )

    return data


# Usage

data = []
ids = get_pubmed_ids("alzheimer")
splitted_ids = split_ids(ids)

for id_list in tqdm(splitted_ids):
    data.append(fetch_pubmed(id_list))

unique_df = pd.concat(data)
print(unique_df)
#unique_df.to_json("pubmed_data.json", orient="records", lines=True)
#unique_df.to_hdf("pubmed_data.h5", key="pubmed_data", mode="w")
