# main.py
from dotenv import load_dotenv
import os
import pandas as pd
from data_fetcher import GooglePlacesFetcher
from data_comparator import DataComparator
from data_formatter import format_address, format_phone_number, format_zip

def main():
    load_dotenv()
    api_key = os.getenv('GOOGLE_API_KEY')
    fetcher = GooglePlacesFetcher(api_key)

    # Load business data from CSV
    df = pd.read_csv("/Users/pedro/Documents/GitHub/BBBdatagetsbetter/Data_Processing/Output_Data/cleaned_and_normalized_data_all.csv", nrows=25)

    df['phone'] = df['phone'].apply(format_phone_number)
    df['zip'] = df['zip'].apply(format_zip)

    # Create a list to store updated rows
    updated_rows = []

    # Iterate through each business entry and verify
    for _, row in df.iterrows():

        company_name = row["company_name"]
        city = row["city"]
        state = row["state"]
        address = row["address"]
        zip_code = row["zip"]
        phone = row["phone"]
        formatted_address = format_address(address, city, state, zip_code)
        print(formatted_address)

        # Construct query for Google Places API
        query = f"{company_name} {city}, {state}"

        # Retrieve business information from API
        api_data = fetcher.fetch_data(query)
        print(api_data)


        updated_row = row.copy()
        if api_data:
            confidence_score = DataComparator.calculate_confidence(row, formatted_address, api_data)

            # If business is not found in Google Places
            if confidence_score == -1:
                updated_row["outdated"] = True
                updated_row["outdated_reason"] = "No match found in Google Places"
            else:
                updated_row['confidence_score'] = confidence_score
                updated_row = DataComparator.update_outdated_info(updated_row, formatted_address, api_data, confidence_score)
        else:
            updated_row['outdated'] = True
            updated_row['outdated_reason'] = "No data found in the API"
        updated_rows.append(updated_row)

    updated_df = pd.DataFrame(updated_rows)
    updated_df.to_csv("/Users/pedro/Documents/GitHub/BBBdatagetsbetter/BBB_Library/Data/updated_business_data.csv", index=False)
    print("Business information verification complete. Updated data saved to 'updated_business_data.csv'")

if __name__ == "__main__":
    main()
