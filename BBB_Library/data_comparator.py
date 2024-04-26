# data_comparator.py
from fuzzywuzzy import fuzz

class DataComparator:
    @staticmethod
    def calculate_confidence(local_data, local_formatted_address, api_data):

        print("Debugging calculate_confidence entry:")
        print("Local Name:", local_data.get('company_name'))
        print("API Data Name:", api_data.get("name"))
        # Check name similarity first
        if DataComparator.check_name_similarity(local_data['company_name'], api_data):

            api_name = str(api_data.get("name", ""))
            api_address = str(api_data.get("formatted_address", "").replace(", USA", ""))
            api_phone = str(api_data.get("formatted_phone_number", "")).replace(" ", "").replace("-", "").replace("(", "").replace(")", "")\
            
            print("Comparing:")
            print(local_data['company_name'])
            print(api_name)
            print(local_formatted_address)
            print(api_address)
            print(local_data['phone'])
            print(api_phone)

            address_score = fuzz.ratio(local_formatted_address, api_address)
            phone_score = 100 if local_data['phone'] == api_phone else 0

            address_weight = 0.5
            phone_weight = 0.5

            confidence_score = (address_score * address_weight) + (phone_score * phone_weight)
            return confidence_score
        else:
            return -1  # Return -1 if names don't match sufficiently

    @staticmethod
    def update_outdated_info(local_data, local_fomatted_address, api_data, confidence_score):
        outdated_reason = ""
        api_address = str(api_data.get("formatted_address", "").replace(", USA", ""))
        api_phone = str(api_data.get("formatted_phone_number", "")).replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        api_name = str(api_data.get("name", ""))
        api_url = api_data.get("website", "")

        if confidence_score < 80:
            if fuzz.ratio(local_fomatted_address, api_address) < 80:
                outdated_reason += "Address mismatch, "
            if local_data['phone'] != api_phone:
                outdated_reason += "Phone mismatch, "

            # Remove trailing comma if present
            outdated_reason = outdated_reason.rstrip(", ")

            local_data['outdated_reason'] = outdated_reason
            local_data['outdated'] = True
        else:
             # Explicitly mark as not outdated if the conditions are not met
            local_data["outdated"] = False
            local_data["outdated_reason"] = "Information current" 
        
        local_data["google_name"] = api_name
        local_data["google_address"] = api_address
        local_data["google_phone"] = api_phone
        local_data["google_url"] = api_url
        local_data["google_place_id"] = api_data.get("place_id", "")

        return local_data

    @staticmethod
    def check_name_similarity(company_name, api_data):
        api_name_str = str(api_data.get("name", ""))
        name_similarity_score = fuzz.ratio(company_name, api_name_str)
        return name_similarity_score >= 70  # Returns True if names are close enough
