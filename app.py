from flask import Flask, render_template, request, redirect, url_for
import pickle
import requests
from bs4 import BeautifulSoup
import re
global fertilizer_name
app = Flask(__name__)

# Load the machine learning models from pickle files
model = pickle.load(open('classifier.pkl', 'rb'))
fertilizer = pickle.load(open('fertilizer.pkl', 'rb'))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        temp = int(request.form.get('field5'))  # Correct the field names
        humi = int(request.form.get('field4'))
        mois = int(request.form.get('field6'))
        soil = int(request.form.get('dropdown1'))
        crop = int(request.form.get('dropdown2'))
        nitro = int(request.form.get('field1'))
        pota = int(request.form.get('field3'))
        phosp = int(request.form.get('field2'))

        input = [temp, humi, mois, soil, crop, nitro, pota, phosp]

        # Use the loaded model to make predictions
        result = fertilizer.classes_[model.predict([input])[0]]

        
        fertilizer_name = result


        # Redirect to the result page with the prediction result
        return redirect(url_for('result', prediction=result))

    return render_template('index.html')



@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        # Assuming the form inputs are sent as POST data
        area_land = request.form.get('field1')
        water_pump = request.form.get('dropdown2')
        tractor_spraying = request.form.get('dropdown3')
        
        # Assuming 'prediction' is passed as a query parameter
        prediction = request.args.get('prediction', '')
        return redirect(url_for('fetch_price', prediction=prediction))

        # return render_template('result.html', prediction=prediction, area_land=area_land, water_pump=water_pump, tractor_spraying=tractor_spraying)
    else:
        prediction = request.args.get('prediction', '')
        return render_template('result.html', prediction=prediction)




@app.route('/fetchprice', methods=['GET', 'POST'])
def fetch_price():
    if request.method == 'GET':
        prediction = request.args.get('prediction', '')
        fertilizer_name2 = prediction

        urea_url = 'https://gogarden.co.in/products/urea-fertilizers-for-plants-46-nitrogen-fertilizer-soil-application-and-100-water-soluble-1?variant=45157595316497'
        dap_url = 'https://indiangardens.in/products/copy-of-dap-fertilizer-for-all-plant-1-kg'
        twenty_twenty_url = 'https://gogarden.co.in/products/npk-20-20-20-water-soluble-fertilizer-for-plants-or-abundant-flowering-and-plant-growth-fertilizer-for-home-plants-100-water-soluble-400-gm-pack'

        urea_price_class = 'price-item price-item--regular'  # Replace with the actual class name
        dap_price_class = 'price-item price-item--regular'  # Replace with the actual class name
        twenty_twenty_price_class = 'price-item price-item--sale'  # Replace with the actual class name

        if fertilizer_name2.lower() == 'urea':
            price = get_fertilizer_price('urea', urea_url, urea_price_class)
        elif fertilizer_name2.lower() == 'dap':
            price = get_fertilizer_price('dap', dap_url, dap_price_class)
        elif fertilizer_name2.lower() == '20-20-20':
            price = get_fertilizer_price('20-20-20', twenty_twenty_url, twenty_twenty_price_class)
        else:
            price = None

        if price is not None:
            return render_template('fertilizer.html', fertilizer_name=fertilizer_name2, price=price)
        else:
            return render_template('fertilizer.html', fertilizer_name=fertilizer_name2, price="Failed to fetch price.")

    return render_template('fertilizer.html')


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

if __name__ == '__main__':
    app.run(debug=True)