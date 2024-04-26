# BBB Data Gets Better and Better

This README provides a detailed description of each script in this repository and the recommended order for executing them.

## Overview

The scripts in this repository are designed for processing and validating data from the BBB (Better Business Bureau) database. They help in merging, cleaning, normalizing, and matching records with an external, more up-to-date database.

## Data Processing

### Merge

**Scripts:** `merge_add_ph.py` and `merge.py`

**Description:**  
This script merges several CSV files from the BBB database, including:
- `tblfirms_firm_companyname.csv`
- `tblfirms_firm_address.csv`
- `tblfirms_firm_phone.csv`
- `tblfirms_firm_email.csv`
- `tblfirms_firm_url.csv`
- `tblfirms_firm.csv`

It combines essential information such as company name, address, phone number, email, website URL, and business status (active or out of business).

**Execution Order:**
1. `merge_add_ph.py`
2. `merge.py`

### Clean and Normalize

**Script:** `clean_and_normalize.py`

**Description:**  
After merging the data, this script elimates invalid entries, filters out businesses that are out of business, selects the wanted columns and formats the data types as needed.

## BBB Library

**Location:** `BBB_Library` folder

**Description:**  
The BBB Library contains scripts for record matching and validation using the cleaned and normalized CSV file. These scripts match BBB's database records with another database (referred to here as "model"), which is believed to be more up-to-date. The library includes methods such as fetching data from Google Places. This library opens the possibility for new "models" to be added.

**Requirements for new models:**
- Output must be JSON with the following information: business name, adress, phone number, and website. It should be in the specified format:
  - `name`
  - `formatted_address`
  - `formatted_phone_number`
  - `website`

This format ensures that all essential business information is standardized and ready for further processing or integration with the library's methods.

## Verifying Business Records based on Google Places API

#### Introduction

This documentation explains a Python library designed to verify business information using Google's Places API.

#### Overview

The library operates in several stages:

1. **Loading Environment Variables**: It begins by loading sensitive data (like API keys) securely from a hidden file (.env) to access Google's API.
2. **Defining Functions**: Several functions are defined to handle different tasks like fetching data from Google, calculating the confidence score, and updating the business information based on fetched data.
3. **Processing Data**: The script reads a list of businesses, checks each one against Google's database, and updates the records with new information and a confidence score.
4. **Saving the Updated Data**: Finally, it saves the updated business information back to a file.

#### Key Function: Calculating the Confidence Score

The "confidence score" is a pivotal part of this script. It quantifies how reliable the existing business data is compared to the data fetched from Google's API. Here's a simplified explanation of how this score is computed:

- **Inputs**: The function takes in the known business details (company name, address, and phone number) and the corresponding data retrieved from Google.
- **Normalization**: The script formats both the input and Google's data to ensure they are in a consistent format. For instance, it removes spaces and special characters from phone numbers.
- **Comparison**: Each piece of information (name, address, phone number) is compared between the existing data and Google’s data. The comparison of addresses and names uses a method called "fuzzy matching," which scores how similar two strings are. Phone numbers are checked for an exact match.
- **Scoring**:
  - **Address Matching**: Uses fuzzy matching to score similarity, contributing 50% to the overall confidence score.
  - **Phone Matching**: Contributes 50% to the overall score. It gives a perfect score (100%) if the phone numbers match exactly; otherwise, it scores 0%.
- **Weighted Average**: The scores from the address and phone are averaged based on their weights to produce the final confidence score.

#### Decision Based on Confidence Score

After the confidence score is calculated, the script determines whether the business information is outdated:

- **Threshold**: A score below 80% is considered unreliable. The script then checks which data points (address, phone) contributed to the low score and notes the mismatches.
- **Updating Records**: Based on these checks, the business record is updated with the new information and the reasons it's considered outdated.

#### Conclusion

This script automates the verification of business listings by comparing them against authoritative data from Google. The confidence score is a robust metric used to gauge the accuracy of the information, ensuring that business listings are up-to-date and reliable.

## Limitations and Solutions

### Address Normalization Challenges

#### Inconsistencies in Address Formatting

The BBB database entries may feature varying formats for addresses. For example, an address in the BBB database might be listed as:
- Full Format: `1234 Boulevard Maple Street, Springfield, MN 62704`
- Abbreviated Format: `1234 Blvd. Maple Street, Springfield, MN 62704`

Google Places API, on the other hand, consistently uses abbreviated formats for street names. This discrepancy can lead to issues in matching and validating addresses between the two sources.

#### Normalization with USAaddress

**Script:** `address_normalizer.py`

This script employs the `usaddress` library to attempt standardizing BBB addresses to their abbreviated formats. Although effective in many cases, there are exceptions where the normalization process does not perform as expected. For instance:
- Original: `1408 County Road C West, Roseville, MN 55113`
- Normalized Incorrectly: `1408 C Roseville, MN 55113`

Additionally, the script does not currently handle variations such as `NW` versus `NORTHWEST`.

### Solution: Fuzzy Matching

To address these inconsistencies, we've implemented a fuzzy matching approach using the `fuzzywuzzy` library. This method helps to bridge the gap between different formatting styles by allowing a degree of textual similarity rather than exact matches.

#### Fuzzy Testing

**Location:** `FuzzyTesting` folder

**Script:** `test.py`

This script evaluates the effectiveness of the fuzzy matching process by comparing abbreviated addresses with their full-text counterparts. Our testing indicates that `fuzzywuzzy` can confidently achieve a similarity match of over 90% for such cases, making it a reliable solution for overcoming the described limitations.

This approach allows us to trust the matching process despite the noted discrepancies in address formatting, ensuring higher accuracy in our data integration tasks.

## Documentation for Identifying Duplicates Within a Dataset

### Introduction

This documentation explains a Python script designed to identify duplicate records within a dataset using the Python Record Linkage Toolkit.

### Overview

This script operates in four stages:

1. **Loading Data**: The pre-processed business record data is fed into the script using the load_data function. This data is then preprocessed further by ensuring correct data typing of the firm ID and the phone number and by creating a unique primary key called "ID".
2. **Indexing Records**: All possible duplicate record pairs are created using a blocking method that divides the records within groups which have a high likelihood of being duplicate records. These duplicate record pairs are known as candidate links.
3. **Computing Similarity Score**: Each candidate link is evaluated based on their similarity of company name, address, state, email, and url. These feature similarities are calculated and saved in a dataframe called "features." These features are then ranked to determine the best matches using a threshold which are saved in a dataframe called "matches".
4. **Identifying Duplicate Records**: Using the unique "ID" of each paired record in matches, the firm ID is extracted from the original record data and placed into a list of tuples. These pairs of firm IDs signify which business records were identified as duplicates. At the end of this process, the list of duplicate record pairs are outputted in a csv named "duplicate_records."

### Data Deduplication

**Location:** `BBB_Library` folder
**Script:** `data_deduplication`

This script contains functions relevant to identify duplicate records within a dataset. It is meant to be used with the cleaned and merged dataset from the data processing section.

### Functions

#### load_data()

This function loads data from a CSV file and returns a loaded dataframe using a file path as input. It ensures that the firm id and phone number are formatted as strings. It also sets a key to uniquely identify each business record in the dataframe. 

#### data_indexer()

This function uses the Python recordlinkage toolkit to create a data indexer to generate candidate links based on a specific subset of features in the dataset. Based on testing, the indexer blocks the company name and the address to generate probable duplicate record matches. 

#### compute_features()

This function uses the candidate links generated by data_indexer() to compute the similarity scores of specific features using the recordLinkage.Compare() object. The criteria to evaluate these features can either be string, numeric, or exact. Default threshold values are used based on testing but these can be tweaked for future use. Additionally, more features can be added to the comparision. For more information on various comparison methods, visit the recordLinkage documentation.

Features dataframe

![image](https://github.com/TebibuS/BBBdatagetsbetter/assets/112585051/6ac7bbf2-59f0-45bb-8ad4-d14d5858c4e5)

#### compute_matches()

This function uses the features dataframe generated by compute_features() and returns a dataframe of the records that have the highest total similarity score based on a pre-defined threshold. It also denotes an ID column for each record pair to be used. 

*Note that if more features are added for comparison in compute_features() the threshold must be changed. Each feature has a maximum value of 1 which denotes a 100% match. The current implementation has 5 features so the default threshold for a match is a 4.5.

#### get_matches()

This function takes the unique ID's generated by compute_matches() and finds the firm ID of that record in the orginal dataset. Once the firm ID is found for both records in the record pair, it adds the record pair's firm ID into a list of tuples which is returned by the function. A helper function called get_firm_id is used to grab the firm ID using a specific ID value in the matches dataframe.   

#### deduplication()

This function is intended to be the main function for something using the `data_deduplication` module. It contains methods from every function used to simplifiy the data deduplication process for the end user. The only input paramerters is the path to the cleaned and merged dataset and the function outputs a csv file containing record pairs of all the duplicate records identified by the script. 

#### How to Use

To use these functions to identify duplicated records, use the deduplication function. This function takes the path to the merged and clean data and the desired threshold for potential matches. It outputs a csv with the firm IDs of duplicate record pairs. Note that the threshold mentioned in the parameters only impacts the criteria for generating matches from the total similarity score. For more specific threshold tweaking, see the compute_features function.

Example of using data_deduplication
```
import data_deduplication as dedup
result = dedup.deduplication('C:\BBBdatagetsbetter\Data\cleaned_and_normalized_data_all.csv',4.5)
```

