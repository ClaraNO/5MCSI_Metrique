from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route("/")
def hello_world():
    return render_template('hello.html') #CommitPageDeCo

@app.route("/contact/")
def MaPremiereAPI():
    return render_template('contact.html')

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")

@app.route('/commits')
def get_commits():
    # Connexion à la base de données SQLite
    conn = sqlite3.connect('path_to_your_database.db')  # Remplacez par le chemin de votre base de données
    cursor = conn.cursor()

    # Exécution de la requête pour récupérer les commits
    cursor.execute("SELECT date FROM commits")  # Adaptez la requête selon votre schéma de base de données
    commits = cursor.fetchall()

    # Fermeture de la connexion
    conn.close()

    # Extraction des minutes
    commits_minutes = [datetime.strptime(commit[0], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M') for commit in commits]

    # Rendre le template avec les données des minutes
    return render_template('commits.html', commits_minutes=commits_minutes)


if __name__ == "__main__":
  app.run(debug=True)
