from flask import Flask, render_template, request, redirect, url_for
import pickle

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

        global fertilizer_name
        fertilizer_name = result


        # Redirect to the result page with the prediction result
        return redirect(url_for('result', prediction=result))

    return render_template('index.html')

@app.route('/result')

def result():
    prediction = request.args.get('prediction')
    return render_template('result.html', prediction=prediction)


if __name__ == '__main__':
    app.run(debug=True)