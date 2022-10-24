from flask import Flask, render_template, request
from flight_emissions import calculate_emissions

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    origin = request.form.get('origin-select')
    destination = request.form.get('destination-select')
    n_pax = request.form.get('num-pax')
    rt = request.form.get('round-trip')
    radf = request.form.get('rad-force')

    #if (origin == "None") or (destination == "None"):
    output = ""
    if (origin is not None) & (destination is not None):
        try:
            tonnes = calculate_emissions(origin, destination, rt, radf, n_pax)
            output = f'<div id="output-div">Your Flight from {origin} to {destination} output {tonnes} tonnes of CO2</div>'
        except:
            output = "<b style='color:red;'>Check your input values and try again. Confirm correct IATA codes</b>"

    return render_template('index.html', emissions=output)

