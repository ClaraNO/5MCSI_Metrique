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

@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    try:
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        minutes = date_object.minute
        return jsonify({'minutes': minutes})
    except ValueError as e:
        return jsonify({'error': 'Invalid date format', 'details': str(e)}), 400

@app.route('/commits/')
def commits_graph():
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    
    try:
        # Effectuer une requête GET à l'API GitHub
        response = requests.get(url)
        response.raise_for_status()  # Assurez-vous que la requête a réussi
        
        commits_data = response.json()
        
        # Extraire les minutes des commits en utilisant la route /extract-minutes/
        commits_minutes = []
        for commit in commits_data:
            commit_date = commit['commit']['author']['date']
            # Utiliser la route extract-minutes pour obtenir les minutes
            minute_response = requests.get(f'http://localhost:5000/extract-minutes/{commit_date}')
            if minute_response.status_code == 200:
                minute_data = minute_response.json()
                commits_minutes.append(minute_data['minutes'])
            else:
                return jsonify({'error': 'Erreur lors de l\'extraction des minutes', 'details': minute_response.json()}), 500
        
        # Vérification : Si pas de données
        if not commits_minutes:
            return jsonify({'error': 'Aucun commit trouvé'}), 404
        
        # Passer les données des minutes au template
        return render_template('commits.html', commits_minutes=commits_minutes)
    
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Erreur lors de la récupération des données de l\'API GitHub', 'details': str(e)}), 500


if __name__ == "__main__":
  app.run(debug=True)
