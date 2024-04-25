# data_formatter.py

def format_address(address, city, state, zip_code):
    return f"{address}, {city}, {state} {zip_code}"

def format_phone_number(phone_str):
    if phone_str and isinstance(phone_str, str) and phone_str.endswith('.0'):
        return phone_str[:-2]
    return phone_str
