import random
from fuzzywuzzy import fuzz

# Define the function to standardize address formats
def standardize_address(address):
    replacements = {
        'Street': 'St.',
        'Avenue': 'Ave.',
        'Boulevard': 'Blvd.',
        'Drive': 'Dr.',
        'Road': 'Rd.'
    }
    for long, short in replacements.items():
        address = address.replace(long, short)
    return address

# Function to calculate similarity of each address against a standardized format
def evaluate_address_similarities(addresses):
    results = []
    print("Comparing Addresses:")
    for address in addresses:
        standardized_address = standardize_address(address)
        similarity_score = fuzz.ratio(address, standardized_address)
        results.append(similarity_score)
        print(f"Original: {address}")
        print(f"Standardized: {standardized_address}")
        print(f"Similarity Score: {similarity_score}\n")
    return results

# Generate fake addresses
def generate_addresses(num_addresses):
    street_suffixes = ['Rd.', 'Road', 'St.', 'Street', 'Ave.', 'Avenue', 'Blvd.', 'Boulevard', 'Dr.', 'Drive']
    cities = ['Minneapolis', 'Saint Paul', 'Bloomington', 'Edina', 'Richfield', 'Brooklyn Park', 'Maple Grove']
    states = ['MN', 'WI', 'IA', 'IL', 'ND', 'SD']

    fake_addresses = []
    for _ in range(num_addresses):
        street_number = random.randint(100, 9999)
        street_name = f'{street_number} Industrial {random.choice(street_suffixes)} NE'
        city = random.choice(cities)
        state = random.choice(states)
        zip_code = f'{random.randint(10000, 99999)}'
        address = f'{street_name}, {city}, {state} {zip_code}'
        fake_addresses.append(address)

    return fake_addresses

# Main function to run the program
def main():
    num_addresses = 50  # Number of addresses to generate
    addresses = generate_addresses(num_addresses)
    similarity_scores = evaluate_address_similarities(addresses)
    average_similarity = sum(similarity_scores) / len(similarity_scores)
    
    print(f'Average Similarity: {average_similarity}%')
    print('Sample Similarity Scores:', similarity_scores[:5])

if __name__ == "__main__":
    main()
