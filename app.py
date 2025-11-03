from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

""" @app.route('/run_prono', methods=['POST'])
def run_prono():
    equipo = request.form['equipo']
    fecha = int(request.form['fecha'])
    pos_local = int(request.form['pos_local'])
    pos_visitante = int(request.form['pos_visitante'])

    resultats = getContextoLocalFechaData(equipo, fecha, pos_local, pos_visitante)
    return render_template('index.html', resultats=resultats) """

if __name__ == '__main__':
    print("🚀 Serveur Flask démarré sur http://127.0.0.1:5000")
    app.run(debug=True)
