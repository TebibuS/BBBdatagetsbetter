import pandas as pd

address_df = pd.read_csv('Data_Processing/Source_Data/tblfirms_firm_address.csv', low_memory=False)
phone_df = pd.read_csv('Data_Processing/Source_Data/tblfirms_firm_phone.csv', low_memory=False)

# Sort by 'main' in descending order so True comes before False
#phone_df_sorted = phone_df.sort_values(by='main', ascending=False)

# Drop duplicates, keeping the first occurrence
phone_df_deduplicated = phone_df.drop_duplicates(subset=['address_id_p'], keep='first')

# Merge phone numbers with addresses based on matching address IDs
phone_address_merged = pd.merge(address_df, phone_df_deduplicated, left_on='address_id_a', right_on='address_id_p', how='left', suffixes=('_address', '_phone'))
#print("Merged DataFrame columns:", phone_address_merged.columns)
# Now, phone_address_merged contains each phone number matched with its corresponding address.
# You can select the columns you need from this merged DataFrame. For example:
phone_address_selected = phone_address_merged[['firm_id_address', 'phone', 'address_1', 'city', 'state', 'zip', 'address_id_a', 'address_id_p']]
phone_address_selected = phone_address_selected.rename(columns={'firm_id_address': 'firm_id'})

phone_address_selected.to_csv('Data_Processing/Output_Data/address_phones_all.csv', index=False)