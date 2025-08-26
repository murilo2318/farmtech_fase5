from flask import Flask, render_template, jsonify
from flask_mysqldb import MySQL
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/sensors')
def get_sensors():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nome, tipo, status, localizacao, data_instalacao FROM sensores")
    rows = cur.fetchall()
    cur.close()
    sensors = [
        {"id": r[0], "nome": r[1], "tipo": r[2], "status": r[3], "localizacao": r[4], "data_instalacao": r[5].isoformat()}
        for r in rows
    ]
    return jsonify(sensors)

@app.route('/api/temperature')
def get_temperature():
    cur = mysql.connection.cursor()
    cur.execute("SELECT dia, temperatura FROM temperatura ORDER BY dia ASC LIMIT 7")
    rows = cur.fetchall()
    cur.close()
    data = [{"dia": r[0].isoformat(), "temperatura": r[1]} for r in rows]
    return jsonify(data)

@app.route('/api/humidity')
def get_humidity():
    cur = mysql.connection.cursor()
    cur.execute("SELECT dia, umidade FROM umidade ORDER BY dia ASC LIMIT 7")
    rows = cur.fetchall()
    cur.close()
    data = [{"dia": r[0].isoformat(), "umidade": r[1]} for r in rows]
    return jsonify(data)

@app.route('/api/yield')
def get_yield():
    cur = mysql.connection.cursor()
    cur.execute("SELECT cultura, modelo, previsto, realizado FROM produtividade")
    rows = cur.fetchall()
    cur.close()
    data = [{"cultura": r[0], "modelo": r[1], "previsto": r[2], "realizado": r[3]} for r in rows]
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
