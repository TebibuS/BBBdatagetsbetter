# data_formatter.py
import pandas as pd
from address_normalizer import normalizer


def format_address(address, city, state, zip_code):
    form = f"{address}, {city}, {state} {zip_code}"
    return form

def format_phone_number(phone_float):
    if phone_float and not pd.isna(phone_float):
        phone_str = str(int(phone_float))
        return phone_str
    return ""

def format_zip(zip_float):
    if zip_float and not pd.isna(zip_float):
        zip_str = str(int(zip_float))
        return zip_str
    return ""
