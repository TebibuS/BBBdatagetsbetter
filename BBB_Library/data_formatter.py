# data_formatter.py
import pandas as pd

def format_address(address, city, state, zip_code):
    # Formats a complete address string using address components.
    form = f"{address}, {city}, {state} {zip_code}"
    return form

def format_phone_number(phone_float):
    # Converts a phone number from float to a string format, removing decimals.
    # Returns an empty string if the input is None or NaN.
    if phone_float and not pd.isna(phone_float):
        phone_str = str(int(phone_float))
        return phone_str
    return ""

def format_zip(zip_float):
    # Converts a ZIP code from float to a string format, removing decimals.
    # Returns an empty string if the input is None or NaN.
    if zip_float and not pd.isna(zip_float):
        zip_str = str(int(zip_float))
        return zip_str
    return ""
