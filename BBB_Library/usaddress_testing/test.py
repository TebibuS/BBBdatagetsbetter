import usaddress

# Define a sample address
sample_address = '123 Main St, Springfield, IL 62701'

# Parse the address using usaddress
parsed_address, address_type = usaddress.tag(sample_address)

# Print the parsed address components and the type of address
print("Parsed Address Components:", parsed_address)
print("Address Type:", address_type)


def test_address_parsing(address):
    try:
        parsed_address, _ = usaddress.tag(address)
        print(f"Original Address: {address}")
        print("Parsed Address:", parsed_address)
        print("-----")
    except Exception as e:
        print(f"Failed to parse address: {address}. Error: {e}")

# List of sample addresses to test
addresses = [
    '123 Main St, Springfield, IL 62701',
    'PO Box 321, Springfield, IL 62701',
    '456 Elm St Apt 789, Springfield, IL 62701',
    '1000 Park Avenue, New York, NY 10022',
    'Suite 200, 250 Peachtree Street, Atlanta, GA 30303'
]

for address in addresses:
    test_address_parsing(address)
