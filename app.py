
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle form submission here
        # You can access form data using request.form.get('field_name')
        # Example: field1 = request.form.get('field1')
        pass
        return redirect(url_for('result'))
    return render_template('index.html')


@app.route('/result')
def result():
    return render_template('result.html')


if __name__ == '__main__':
    app.run(debug=True)
