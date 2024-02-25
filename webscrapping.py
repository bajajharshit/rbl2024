import requests
from bs4 import BeautifulSoup
import re

def extract_integer_price(price_string):
    # Extract only the numeric part from the string
    numeric_part = re.search(r'\b(\d+(\.\d+)?)\b', price_string)

    if numeric_part:
        price_as_string = numeric_part.group(1)
        # Convert the numeric part to an integer
        fertilizer_price = int(float(price_as_string))  # Convert to float first to handle decimal points
        return fertilizer_price
    else:
        return None  # No numerical value found in the string.

def get_fertilizer_price(fertilizer_name, url, price_class):
    # Get the URL for the specified fertilizer
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Adjust the code to extract the price based on the HTML structure of the website
        # This is just an example, you need to inspect the actual structure of the websites
        price_element = soup.find('span', {'class': price_class})

        if price_element:
            price_as_string = price_element.text.strip().replace('Rs.', '').replace(',', '').strip()
            fertilizer_price = extract_integer_price(price_as_string)
            if(fertilizer_name == '20-20-20') : return fertilizer_price*12.5
            return fertilizer_price
        else:
            return None  # Price information not found
    else:
        return None  # Failed to retrieve data

# Example usage:
urea_url = 'https://gogarden.co.in/products/urea-fertilizers-for-plants-46-nitrogen-fertilizer-soil-application-and-100-water-soluble-1?variant=45157595316497'
dap_url = 'https://indiangardens.in/products/copy-of-dap-fertilizer-for-all-plant-1-kg'
twenty_twenty_url = 'https://gogarden.co.in/products/npk-20-20-20-water-soluble-fertilizer-for-plants-or-abundant-flowering-and-plant-growth-fertilizer-for-home-plants-100-water-soluble-400-gm-pack'

urea_price_class = 'price-item price-item--regular'  # Replace with the actual class name
dap_price_class = 'price-item price-item--regular'  # Replace with the actual class name
twenty_twenty_price_class = 'price-item price-item--sale'  # Replace with the actual class name

fertilizer_name = input("Enter the fertilizer name (urea, dap, 20-20-20): ")

if fertilizer_name.lower() == 'urea':
    price = get_fertilizer_price('urea', urea_url, urea_price_class)
elif fertilizer_name.lower() == 'dap':
    price = get_fertilizer_price('dap', dap_url, dap_price_class)
elif fertilizer_name.lower() == '20-20-20':
    price = get_fertilizer_price('20-20-20', twenty_twenty_url, twenty_twenty_price_class)
else:
    price = None

if price is not None:
    print(f"The current price of {fertilizer_name} is: Rs. {price}")
else:
    print("Failed to fetch price.")


