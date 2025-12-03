from flask import Flask, render_template, jsonify
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3

app = Flask(__name__)


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
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15  # Conversion de Kelvin en °C
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)


@app.route('/')
def hello_world():
    return render_template('hello.html')


@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")


@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")


# 🔹 API qui renvoie les données de commits (minutes + nombre de commits)
@app.route("/commits_data/")
def commits_data():
    # API GitHub fournie dans l'énoncé
    response = urlopen('https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))

    minutes_count = {}

    for commit in json_content:
        # Récupérer la date du commit : commit -> commit -> author -> date
        date_string = commit.get('commit', {}).get('author', {}).get('date')
        if not date_string:
            continue

        # Exemple de format : "2024-02-11T11:57:27Z"
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        minute = date_object.minute

        # Compter le nombre de commits par minute
        minutes_count[minute] = minutes_count.get(minute, 0) + 1

    # Transformer le dict en liste pour le JSON
    results = []
    for minute, count in sorted(minutes_count.items()):
        results.append({'minute': minute, 'commits': count})

    return jsonify(results=results)


# 🔹 Page HTML qui affiche le graphique
@app.route("/commits/")
def commits():
    return render_template("commits.html")


if __name__ == "__main__":
    app.run(debug=True)
