import streamlit as st
import pickle
import requests
from bs4 import BeautifulSoup
import re




page_element="""
<style>
[data-testid="stAppViewContainer"]{
background-image: url("https://wallpapercave.com/wp/wp3589963.jpg");
background-size: cover;
}
[data-testid="stHeader"]{
background-color: rgba(0,0,0,0);
}
[data-testid="stToolbar"]{
right: 2rem;
background-image: url("");
background-size: cover;
}
[data-testid="stSidebar"]> div:first-child{
background-image: url("https://img.freepik.com/premium-vector/skyblue-gradient-background-advertisers-gradient-hq-wallpaper_189959-513.jpg");
background-size: cover;
}
</style>

"""
st.markdown(page_element, unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;';>जय  जवान  जय  किसान 🚜</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;';>Fertilizer Recommendation 🌿</h1>", unsafe_allow_html=True)
st.markdown("---")


# Load the machine learning models from pickle files
model = pickle.load(open('classifier.pkl', 'rb'))
fertilizer = pickle.load(open('fertilizer.pkl', 'rb'))

# Function to get fertilizer price
def get_fertilizer_price(fertilizer_name, url, price_class):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        price_element = soup.find('span', {'class': price_class})
        if price_element:
            price_as_string = price_element.text.strip().replace('Rs.', '').replace(',', '').strip()
            fertilizer_price = extract_integer_price(price_as_string)
            if(fertilizer_name == '20-20-20') : return fertilizer_price*12.5
            return fertilizer_price
        else:
            return None # Price information not found
    else:
        return None # Failed to retrieve data

# Function to extract integer price
def extract_integer_price(price_string):
    numeric_part = re.search(r'\b(\d+(\.\d+)?)\b', price_string)
    if numeric_part:
        price_as_string = numeric_part.group(1)
        fertilizer_price = int(float(price_as_string)) # Convert to float first to handle decimal points
        return fertilizer_price
    else:
        return None # No numerical value found in the string.

def main():
    if "fertilizer_name" not in st.session_state:
        st.session_state.fertilizer_name = None

    soil_mapping = {'Black': 0, 'Clayey': 1, 'Red': 3}
    crop_mapping = {'Cotton': 0, 'Sugarcane': 1, 'Wheat': 2}
    temp = st.number_input('Temperature', value=20)
    humi = st.number_input('Humidity', value=50)
    mois = st.number_input('Moisture', value=50)
    soil = st.selectbox('Soil Type', options=list(soil_mapping.keys()))
    crop = st.selectbox('Crop Type', options=list(crop_mapping.keys()))
    nitro = st.number_input('Nitrogen', value=10)
    pota = st.number_input('Potassium', value=10)
    phosp = st.number_input('Phosphorus', value=10)
    area_land = st.number_input("Enter total area of land (in acres)", min_value=0, step=1)
    water_pump = st.selectbox("Are you using a water pump?", ["No", "Yes"])
    tractor_spraying = st.selectbox("Are you using a tractor for spraying?", ["No", "Yes"])
    crop = st.selectbox("Select the crop", ["Wheat", "Sugarcane", "Cotton"])

    if st.button('Predict') and st.snow():

        soil_value = soil_mapping[soil]
        crop_value = crop_mapping[crop]
        input = [temp, humi, mois, soil_value, crop_value, nitro, pota, phosp]
        result = fertilizer.classes_[model.predict([input])[0]]
        st.info(f'Recommended Fertilizer: {result}', icon="ℹ️")

        urls = {
            'urea': 'https://gogarden.co.in/products/urea-fertilizers-for-plants-46-nitrogen-fertilizer-soil-application-and-100-water-soluble-1?variant=45157595316497',
            'dap': 'https://indiangardens.in/products/copy-of-dap-fertilizer-for-all-plant-1-kg',
            '20-20-20': 'https://gogarden.co.in/products/npk-20-20-20-water-soluble-fertilizer-for-plants-or-abundant-flowering-and-plant-growth-fertilizer-for-home-plants-100-water-soluble-400-gm-pack'
        }
        price_classes = {
            'urea': 'price-item price-item--regular',
            'dap': 'price-item price-item--regular',
            '20-20-20': 'price-item price-item--sale'
        }


        def extract_integer_price(price_string):
            numeric_part = re.search(r'\b(\d+(\.\d+)?)\b', price_string)

            if numeric_part:
                price_as_string = numeric_part.group(1)
                fertilizer_price = int(float(price_as_string))  
                return fertilizer_price
            else:
                return None  




        def get_fertilizer_price(fertilizer_name, url, price_class):
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                price_element = soup.find('span', {'class': price_class})
                if price_element:
                    price_as_string = price_element.text.strip().replace('Rs.', '').replace(',', '').strip()
                    fertilizer_price = extract_integer_price(price_as_string)
                    if fertilizer_name == '20-20-20':
                        return fertilizer_price * 12.5
                    return fertilizer_price
                else:
                    return None  
            else:
                return None  


        urea_url = 'https://gogarden.co.in/products/urea-fertilizers-for-plants-46-nitrogen-fertilizer-soil-application-and-100-water-soluble-1?variant=45157595316497'
        dap_url = 'https://indiangardens.in/products/copy-of-dap-fertilizer-for-all-plant-1-kg'
        twenty_twenty_url = 'https://gogarden.co.in/products/npk-20-20-20-water-soluble-fertilizer-for-plants-or-abundant-flowering-and-plant-growth-fertilizer-for-home-plants-100-water-soluble-400-gm-pack'

        urea_price_class = 'price-item price-item--regular'  # Replace with the actual class name
        dap_price_class = 'price-item price-item--regular'  # Replace with the actual class name
        twenty_twenty_price_class = 'price-item price-item--sale'  # Replace with the actual class name

        st.session_state.fertilizer_name = result.lower()
        # st.write(fertilizer_name)
        # st.write(len(fertilizer_name))
        if (st.session_state.fertilizer_name == ' urea'):
            url = urea_url
            price_class= urea_price_class
        elif (st.session_state.fertilizer_name == ' dap'):
            url = dap_url
            price_class= dap_price_class
        elif (st.session_state.fertilizer_name == ' 20-20-20'):
            url = twenty_twenty_url
            price_class= twenty_twenty_price_class

        
        
        price = get_fertilizer_price('urea', url, price_class)

        if price is not None:
            st.info(f"The current price of {st.session_state.fertilizer_name} is: Rs. {price}", icon="💰")
        else:
            st.info("Failed to fetch price.", icon="⚠️")


        # Fetch the price for the recommended fertilizer
        if result in urls:
            url = urls[result]
            price_class = price_classes[result]
            price = get_fertilizer_price(result, url, price_class)
            if price is not None:
                st.write(f'Price: {price}')
            else:
                st.write("Failed to fetch price.")

        if crop == "Wheat":
            if st.session_state.fertilizer_name == " urea":
                min=5
                max=7
            if st.session_state.fertilizer_name == " dap":
                min=4.5
                max=5.5
            if st.session_state.fertilizer_name == " 20-20-20":
                min=10
                max=12.5

        elif crop == "Sugarcane":
            if st.session_state.fertilizer_name == " urea":
                min=12
                max=15
            if st.session_state.fertilizer_name == " dap":
                min=10
                max=12.5
            if st.session_state.fertilizer_name == " 20-20-20":
                min=5
                max=7.5

        elif crop == "Cotton":
            if st.session_state.fertilizer_name == " urea":
                min=9
                max=11
            if st.session_state.fertilizer_name == " dap":
                min=5
                max=6
            if st.session_state.fertilizer_name == " 20-20-20":
                min=5
                max=7.5
        if water_pump == "Yes":
            water_pump_price= 40000
        else:
            water_pump_price= 0

        if tractor_spraying =="Yes":
            tractor_spraying_price= 35000
        else:
            tractor_spraying_price= 0

        calculated_value_min = price*min*area_land + water_pump_price + tractor_spraying_price
        calculated_value_max = price*max*area_land + water_pump_price + tractor_spraying_price
        # st.write(min, max)
        # st.write(price, water_pump_price, tractor_spraying_price)
        # st.write(calculated_value_min, calculated_value_max)

        st.success("The price of the Crop Fertilizer is from Rs. "+ str(calculated_value_min) +" - " + str(calculated_value_max))
        st.write("Price Breakdown -")
        st.write(f"Price of the Feritlizer per acre for {crop} is Rs. {min*price} - {max*price} ")

        if tractor_spraying =="Yes":
            st.write(f"Price of the Tactor Spraying - Rs. {tractor_spraying_price} ")
        if water_pump == "Yes":
            st.write(f"Price of the Water Pump - Rs. {water_pump_price} ")


        # if st.session_state.fertilizer_name and crop:
        #     st.markdown("### Additional Fertilizer Quantity")
        #     if crop == "Wheat" and st.session_state.fertilizer_name == " urea":
        #         slider_min = 50
        #         slider_max = 70
        #     elif crop == "Sugarcane" and st.session_state.fertilizer_name == " dap":
        #         slider_min = 100
        #         slider_max = 400
        #     elif crop == "Cotton" and st.session_state.fertilizer_name == " 20-20-20":
        #         slider_min = 75
        #         slider_max = 300
        #     else:
        #         slider_min = 50
        #         slider_max = 200
            
        #     additional_quantity = st.slider("Select additional quantity (in kg)", slider_min, slider_max, slider_min)

            # if st.button("Calculate Additional Cost"):
            #     additional_cost = additional_quantity * price
            #     st.success(f"The additional cost for {additional_quantity} kg of {st.session_state.fertilizer_name} is: Rs. {additional_cost}")




if __name__ == '__main__':
    main()
