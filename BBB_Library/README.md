### Documentation for Business Information Verification Script

#### Introduction

This documentation explains a Python script designed to verify business information using Google's Places API. The script is intended for users with minimal technical background and will focus primarily on how it calculates a "confidence score" to assess the accuracy of business data against Google's database.

#### Overview of the Script

The script operates in several stages:

1. **Loading Environment Variables**: It begins by loading sensitive data (like API keys) securely from a hidden file (.env) to access Google's API.
2. **Defining Functions**: Several functions are defined to handle different tasks like fetching data from Google, calculating the confidence score, and updating the business information based on fetched data.
3. **Processing Data**: The script reads a list of businesses, checks each one against Google's database, and updates the records with new information and a confidence score.
4. **Saving the Updated Data**: Finally, it saves the updated business information back to a file.

#### Key Function: Calculating the Confidence Score

The "confidence score" is a pivotal part of this script. It quantifies how reliable the data fetched from Google's API is compared to the existing business data. Here's a simplified explanation of how this score is computed:

- **Inputs**: The function takes in the known business details (company name, address, and phone number) and the corresponding data retrieved from Google.
- **Normalization**: The script formats both the input and Google's data to ensure they are in a consistent format. For instance, it removes spaces and special characters from phone numbers.
- **Comparison**: Each piece of information (name, address, phone number) is compared between the existing data and Google’s data. The comparison of addresses and names uses a method called "fuzzy matching," which scores how similar two strings are. Phone numbers are checked for an exact match.
- **Scoring**:
  - **Address Matching**: Uses fuzzy matching to score similarity, contributing 50% to the overall confidence score.
  - **Phone Matching**: Contributes 50% to the overall score. It gives a perfect score (100%) if the phone numbers match exactly; otherwise, it scores 0%.
- **Weighted Average**: The scores from the address and phone are averaged based on their weights to produce the final confidence score.

#### Decision Based on Confidence Score

After the confidence score is calculated, the script determines whether the business information is outdated:

- **Threshold**: A score below 80% is considered unreliable. The script then checks which data points (name, address, phone) contributed to the low score and notes the mismatches.
- **Updating Records**: Based on these checks, the business record is updated with the new information and the reasons it's considered outdated.

#### Conclusion

This script automates the verification of business listings by comparing them against authoritative data from Google. The confidence score is a robust metric used to gauge the accuracy of the information, ensuring that business listings are up-to-date and reliable.