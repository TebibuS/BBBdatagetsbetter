import pandas as pd

# Load the CSV file
final_df = pd.read_csv('Data_Processing/Output_Data/merged_output_all.csv', low_memory=False)

# Drop rows without a company name
final_df.dropna(subset=['company_name'], inplace=True)

# Get the firm ids associated with out of business statuses
out_of_business_firm_ids = final_df[final_df['outofbusiness_status-2'].isin(["Believed to be Out of Business", "Confirmed to be Out of Business"])]['firm_id']

# Drop all rows that have the same firm id as the out of business firms
final_df = final_df[~final_df['firm_id'].isin(out_of_business_firm_ids)]

# Selecting and renaming the desired columns
desired_columns = ['firm_id', 'company_name', 'address_1', 'city', 'state', 'zip', 'phone', 'email', 'url']
final_df = final_df[desired_columns]
final_df.rename(columns={'address_1': 'address'}, inplace=True)

# Normalizing Zip Codes to ensure they are properly formatted as a five-digit string
final_df['zip'] = final_df['zip'].apply(lambda x: f"{int(x):05d}" if pd.notnull(x) and str(x).isdigit() else '')

# Phone Number Formatting to ensure consistency
final_df['phone'] = final_df['phone'].apply(lambda x: f"{int(x):010d}" if pd.notnull(x) and str(x).isdigit() else '')

# Dropping Duplicate Entries based on 'company_name' and 'address'
final_df.drop_duplicates(subset=['company_name', 'address'], inplace=True)

# Saving the cleaned and normalized DataFrame to a new CSV file
final_df.to_csv('Data_Processing/Output_Data/cleaned_and_normalized_data_all.csv', index=False)

print(final_df.head())