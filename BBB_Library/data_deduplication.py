# Data deduplication
import recordlinkage
import pandas as pd
import pathlib

def load_data(path: str) -> pd.DataFrame:
    """
    Load data from a CSV file.

    Args:
        path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Loaded DataFrame.
    """
    record_data = pd.read_csv(path,dtype={'firm_id' : str, 'phone' : str})
    record_data = record_data.reset_index(names=['ID'])
    return record_data

def data_indexer(data: pd.DataFrame) -> pd.MultiIndex:
    """
    Create a data indexer to compute candidate links.

    Args:
        data (pd.DataFrame): DataFrame containing the data.

    Returns:
        pd.MultiIndex: Candidate links for record linkage.
    """
    indexer = recordlinkage.Index()
    indexer.block("company_name")
    indexer.block("address")
    candidate_links = indexer.index(data)
    return candidate_links

def compute_features(data: pd.DataFrame, candidate_links: pd.MultiIndex) -> pd.DataFrame:
    """
    Compute features for candidate record pairs. Default threshold values are set for each feature based on testing. 
    They may be tweaked for future use.

    Computed features can be string, numeric, or exact matches. 
    These functions can be explored more in-depth in the recordLinkage documentation.

    Args:
        data (pd.DataFrame): DataFrame containing the data.
        candidate_links (pd.MultiIndex): Candidate links for record linkage.

    Returns:
        pd.DataFrame: DataFrame containing computed features.
    """
    compare_cl = recordlinkage.Compare()
    compare_cl.string("company_name", "company_name", method="levenshtein", threshold=0.75, label="company_name")
    compare_cl.string("address", "address", method="levenshtein", threshold=0.85, label="address_1")
    compare_cl.exact("state", "state", label="state")
    compare_cl.string("email", "email", method="levenshtein", threshold=0.85, label="email")
    compare_cl.string("url", "url", label="url")
    features = compare_cl.compute(candidate_links, data)
    return features

def compute_matches(features: pd.DataFrame, threshold: float = 4.5) -> pd.DataFrame:
    """
    Compute matches based on computed features.

    Args:
        features (pd.DataFrame): DataFrame containing computed features.
        threshold (float): Threshold for considering a match.

    Returns:
        pd.DataFrame: DataFrame containing matched record pairs.
    """
    matches = features[round(features.sum(axis=1)) >= threshold]
    matches = matches.reset_index(names=['ID1', 'ID2'])
    return matches

def get_matches(data: pd.DataFrame, matches: pd.DataFrame) -> list:
    """
    Get matched 'firm_id' pairs.

    Args:
        data (pd.DataFrame): DataFrame containing the data.
        matches (pd.DataFrame): DataFrame containing matched record pairs.

    Returns:
        list: List of tuples containing matched 'firm_id' pairs.
    """
    def get_firm_id(id_list):
        temp = []
        for id in id_list:
            row = data[data['ID'] == id]
            firm_id = row.iloc[0]['firm_id']
            temp.append(firm_id)
        return temp
    
    id_list1 = matches.ID1.tolist()
    id_list2 = matches.ID2.tolist()
    list1 = get_firm_id(id_list1)
    list2 = get_firm_id(id_list2)
    matches_tuple = [(x, y) for x, y in zip(list1, list2)]
    return matches_tuple

def deduplication(data_path: str, threshold: float = 4.5) -> list[list]:
    """
    Main function to perform data deduplication. Uses all the other functions for ease of 
    use.

    Args:
        data_path (str): Path to the CSV file containing the data.
        threshold (float): Threshold for considering a match.

    Returns:
        list: DataFrame containing matched 'firm_id' pairs of records.
    """
    data = load_data(data_path)
    candidate_records = data_indexer(data)
    features = compute_features(data, candidate_records)
    matches = compute_matches(features, threshold)
    possible_matches = get_matches(data, matches)
    duplicate_records = pd.DataFrame(possible_matches)
    duplicate_records.to_csv("duplicate_records.csv",index=False,header=False)
    return duplicate_records


