# main.py
from dotenv import load_dotenv
import os
import pandas as pd
from data_fetcher import GooglePlacesFetcher
from data_comparator import DataComparator
from data_formatter import format_address, format_phone_number

def main():
    load_dotenv()
    api_key = os.getenv('GOOGLE_API_KEY')
    fetcher = GooglePlacesFetcher(api_key)
    df = pd.read_csv("Data/cleaned_and_normalized_data_first23.csv")

    updated_rows = []
    for _, row in df.iterrows():
        query = f"{row['company_name']} {row['city']}, {row['state']}"
        api_data = fetcher.fetch_data(query)
        if api_data:
            row['formatted_address'] = format_address(row['address'], row['city'], row['state'], row['zip'])
            row['phone'] = format_phone_number(row['phone'])
            confidence_score = DataComparator.calculate_confidence(row, api_data)
            updated_row = DataComparator.update_outdated_info(row, api_data)
            updated_row['confidence_score'] = confidence_score
            updated_rows.append(updated_row)
        else:
            row['outdated'] = True
            row['outdated_reason'] = "No data found"
            updated_rows.append(row)

    updated_df = pd.DataFrame(updated_rows)
    updated_df.to_csv("Data/updated_business_data.csv", index=False)
    print("Business information verification complete. Updated data saved to 'updated_business_data.csv'")

if __name__ == "__main__":
    main()
