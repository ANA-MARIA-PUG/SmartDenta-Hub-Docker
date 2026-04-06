from flask import Flask, render_template, jsonify
from flask_cors import CORS  # Foarte important pentru Docker
import couchdb

app = Flask(__name__)
CORS(app) # Permite browserului să facă cereri către server

# Conectarea la CouchDB folosind numele serviciului din Docker
server = couchdb.Server('http://admin:password@db:5984/')

@app.route('/')
def home():
    return render_template('index.html')

# ACEASTA ESTE RUTA CARE LIPSEȘTE ȘI CAUZEAZĂ EROAREA:
@app.route('/api/<db_name>')
def get_data(db_name):
    try:
        if db_name in server:
            db = server[db_name]
            # Luăm toate documentele (pacienți, doctori etc.)
            data = [db[doc_id] for doc_id in db]
            return jsonify(data)
        else:
            return jsonify({"error": "Baza de date nu exista"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)