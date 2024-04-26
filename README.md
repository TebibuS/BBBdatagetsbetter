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

## Understanding the Library

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


