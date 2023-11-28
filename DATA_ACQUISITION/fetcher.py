import requests
import xml.etree.ElementTree as ET
from tqdm import tqdm
import json
import pandas as pd


def get_pubmed_ids(term, retstart, retmax=50):
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
    esearch_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={term}&retstart={retstart}&retmax={retmax}&format=json&sort=relevance"
    response = requests.get(esearch_url)
    ids = response.json()["esearchresult"]["idlist"]
    all_ids.extend(ids)
    return all_ids


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
retmax = 50
data = []
for i in tqdm(range(100)):
    ids = get_pubmed_ids("Prader Willy", retstart=i * retmax, retmax=retmax)
    data.append(fetch_pubmed(ids))

unique_df = pd.concat(data)

unique_df.to_json("pubmed_data.json", orient="records", lines=True)
unique_df.to_hdf("pubmed_data.h5", key="pubmed_data", mode="w")
