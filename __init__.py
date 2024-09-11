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
    cursor.execute("SELECT id, message, author, date FROM commits")  # Adaptez la requête selon votre schéma de base de données
    commits = cursor.fetchall()

    # Fermeture de la connexion
    conn.close()

    # Transformation des données en JSON
    commits_list = [
        {
            'id': commit[0],
            'message': commit[1],
            'author': commit[2],
            'date': datetime.strptime(commit[3], '%Y-%m-%d %H:%M:%S').isoformat()  # Assurez-vous que le format correspond à celui de votre base de données
        }
        for commit in commits
    ]

    return jsonify(commits_list)


if __name__ == "__main__":
  app.run(debug=True)
