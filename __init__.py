from flask import Flask, render_template, jsonify
from datetime import datetime
from urllib.request import urlopen
import json

app = Flask(_name_)

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))

    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_kelvin = list_element.get('main', {}).get('temp')

        if temp_kelvin is not None:
            temp_celsius = temp_kelvin - 273.15
        else:
            temp_celsius = None

        results.append({'Jour': dt_value, 'temp': temp_celsius})

    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")

@app.route("/commits-data/")
def commits_data():
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    response = urlopen(url)
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))

    results = []
    for commit in json_content:
        date_string = commit.get("commit", {}).get("author", {}).get("date")
        if date_string:
            date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
            results.append(date_object.minute)

    return jsonify(results=results)

@app.route("/commits/")
def commits():
    return render_template("commits.html")

if _name_ == "_main_":
    app.run(debug=True)
