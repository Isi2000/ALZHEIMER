import requests
import numpy as np
import time
import concurrent.futures
import backoff

@backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_time=60)
def fetch_ids_for_month(year, month, term, mail):
    """
    Fetch PubMed IDs for a specific term, year, and month.

    Args:
        year (int): Year for the search.
        month (int): Month for the search.
        term (str): The search term.
        mail (str): Email for API usage.

    Returns:
        list: List of PubMed IDs for the given month and year.
    """
    min_month = month + 1
    max_month = month + 2
    min_date = f"{year}/{min_month:02d}/01"
    if max_month < 13:
        max_date = f"{year}/{max_month:02d}/01"
    else:
        max_date = f"{year+1}/01/01"

    esearch_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={term}&mindate={min_date}&maxdate={max_date}&format=json&email={mail}&retmax=9998"
    response = requests.get(esearch_url)
    if response.status_code == 429:
        raise requests.exceptions.RequestException("Rate Limit Exceeded")
    time.sleep(1)  # Be respectful to the server

    # Print the status code and number of IDs fetched
    print(f"Year: {year}, Month: {month}, Status Code: {response.status_code}, Number of IDs: {len(response.json().get('esearchresult', {}).get('idlist', []))}")

    ids = response.json().get("esearchresult", {}).get("idlist", [])
    return ids

def get_pubmed_ids(term, mail):
    """
    Fetch PubMed IDs for a specific term.

    Args:
        term (str): The search term.
        mail (str): Email for API usage.

    Returns:
        list: List of PubMed IDs.
    """
    all_ids = []
    esearch_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={term}&mindate={800}&maxdate={1990}&format=json&email={mail}&retmax=9998"
    response = requests.get(esearch_url)
    ids = response.json().get("esearchresult", {}).get("idlist", [])
    all_ids.extend(ids)
    years = range(1990, 2023)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_month = {executor.submit(fetch_ids_for_month, year, month, term, mail): (year, month) for year in years for month in range(12)}
        for future in concurrent.futures.as_completed(future_to_month):
            year, month = future_to_month[future]
            try:
                month_ids = future.result()
                all_ids.extend(month_ids)
                print(f"Fetched {len(month_ids)} IDs for {year}-{month}")
            except Exception as exc:
                print(f"{year}-{month} generated an exception: {exc}")

    return all_ids

# Usage
mail = "isacco.faglioni@studio.unibo.it"
ids = get_pubmed_ids("alzheimer", mail)
np.savetxt("ids.csv", ids, delimiter=",", fmt='%s')