import pandas as pd

# Function to add an occurrence order column to a DataFrame based on 'firm_id'
def add_occurrence_order(df, id_column='firm_id'):
    df['occurrence_order'] = df.groupby(id_column).cumcount()
    return df

# Function to merge two DataFrames on 'firm_id' and the occurrence order
def merge_on_occurrence_order(base_df, additional_df, base_columns, additional_columns, suffix=''):
    if 'occurrence_order' not in base_df.columns:
        base_df = add_occurrence_order(base_df)
    additional_df = add_occurrence_order(additional_df)

    # Ensure 'firm_id' in base_df is unique if needed
    base_df['firm_id_unique'] = base_df['firm_id']
    additional_df['firm_id_unique'] = additional_df['firm_id']

    merged_df = pd.merge(base_df[base_columns + ['firm_id_unique', 'occurrence_order']],
                         additional_df[additional_columns + ['firm_id_unique', 'occurrence_order']],
                         left_on=['firm_id_unique', 'occurrence_order'],
                         right_on=['firm_id_unique', 'occurrence_order'],
                         how='left', suffixes=('', suffix))

    merged_df.drop(columns=['firm_id_unique'], inplace=True)  # Drop the temporary unique ID column
    return merged_df

# Load your CSV files
base_df = pd.read_csv('Data_Processing/Source_Data/tblfirms_firm_companyname.csv', low_memory=False)
additional_df_1 = pd.read_csv('Data_Processing/Output_Data/address_phones_all.csv', low_memory=False)
additional_df_2 = pd.read_csv('Data_Processing/Source_Data/tblfirms_firm_email.csv', low_memory=False)
additional_df_3 = pd.read_csv('Data_Processing/Source_Data/tblfirms_firm_url.csv', low_memory=False)
additional_df_4 = pd.read_csv('Data_Processing/Source_Data/tblfirms_firm.csv', low_memory=False)
# Add more DataFrames as needed

# Define the columns you want to keep from each DataFrame (excluding 'firm_id')
base_columns = ['firm_id', 'company_name']
additional_columns_1 = ['address_1', 'city', 'state', 'zip', 'address_id_a','phone', 'address_id_p']
additional_columns_2 = ['email', 'email_id']
additional_columns_3 = ['url']
additional_columns_4 = ['outofbusiness_status-2']
# Add more column lists as needed

# Sequentially merge the DataFrames
merged_df = merge_on_occurrence_order(base_df, additional_df_1, base_columns, additional_columns_1, '_address_phones')
merged_df = merge_on_occurrence_order(merged_df, additional_df_2, base_columns + additional_columns_1, additional_columns_2, '_email')
merged_df = merge_on_occurrence_order(merged_df, additional_df_3, base_columns + additional_columns_1 + additional_columns_2, additional_columns_3,'_url')
merged_df = merge_on_occurrence_order(merged_df, additional_df_4, base_columns + additional_columns_1 + additional_columns_2 + additional_columns_3, additional_columns_4, '_firm')
# Continue merging other DataFrames as needed

# Save the merged DataFrame to a new CSV file
merged_df.to_csv('Data_Processing/Output_Data/merged_output_all.csv', index=False)
