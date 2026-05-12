import os
from flask import Flask, jsonify
from dotenv import load_dotenv

load_dotenv()

from src.routes.flights      import flights_bp
from src.routes.reservations import reservations_bp

app = Flask(__name__)
app.url_map.strict_slashes = False

# Înregistrăm blueprint-urile cu prefixele lor de URL
app.register_blueprint(flights_bp,      url_prefix='/flights')
app.register_blueprint(reservations_bp, url_prefix='/reservations')

# Health check
@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 3003))
    app.run(host='0.0.0.0', port=port)