# data_comparator.py
from fuzzywuzzy import fuzz

class DataComparator:
    @staticmethod
    def calculate_confidence(local_data, api_data):
        address_score = fuzz.ratio(local_data['address'], api_data.get('formatted_address', ""))
        phone_score = 100 if local_data['phone'] == api_data.get('formatted_phone_number', "") else 0

        address_weight = 0.5
        phone_weight = 0.5

        confidence_score = (address_score * address_weight) + (phone_score * phone_weight)
        return confidence_score

    @staticmethod
    def update_outdated_info(local_data, api_data):
        outdated_reason = ""
        if fuzz.ratio(local_data['company_name'], api_data.get('name', "")) < 70:
            outdated_reason += "Name mismatch, "
        if fuzz.ratio(local_data['address'], api_data.get('formatted_address', "")) < 80:
            outdated_reason += "Address mismatch, "
        if local_data['phone'] != api_data.get('formatted_phone_number', ""):
            outdated_reason += "Phone mismatch, "

        outdated_reason = outdated_reason.rstrip(", ")
        local_data['outdated_reason'] = outdated_reason
        local_data['outdated'] = bool(outdated_reason)

        return local_data
