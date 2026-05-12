from flask import Blueprint, request, jsonify
from src.middleware.auth import require_auth, require_admin
from src.services import io_client

# Blueprint = grup de rute, echivalentul router din Express
flights_bp = Blueprint('flights', __name__)

# ============================================================
# GET /flights
# Caută zboruri — rută publică, nu necesită autentificare
# Query params opționali: origin, destination, class, date
# Exemplu: /flights?origin=OTP&destination=LHR&class=economy
# ============================================================
@flights_bp.route('/', methods=['GET'])
def search_flights():
    try:
        # Colectăm filtrele din query string
        params = {}
        if request.args.get('origin'):
            params['origin'] = request.args.get('origin')
        if request.args.get('destination'):
            params['destination'] = request.args.get('destination')
        if request.args.get('class'):
            params['class'] = request.args.get('class')
        if request.args.get('date'):
            params['date'] = request.args.get('date')
        if request.args.get('passengers'):
            params['passengers'] = request.args.get('passengers')

        flights = io_client.get_flights(params)

        # Filtrăm zborurile care nu au destule locuri
        # dacă utilizatorul a specificat numărul de pasageri
        if request.args.get('passengers'):
            passengers = int(request.args.get('passengers'))
            flights = [f for f in flights if f['available_seats'] >= passengers]

        return jsonify(flights)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================
# GET /flights/:id
# Detalii zbor — rută publică
# ============================================================
@flights_bp.route('/<int:flight_id>', methods=['GET'])
def get_flight(flight_id):
    try:
        flight = io_client.get_flight(flight_id)
        return jsonify(flight)
    except Exception as e:
        return jsonify({'error': str(e)}), 404


# ============================================================
# POST /flights
# Adaugă zbor nou — doar admin
# Body: { origin, destination, departure_time, arrival_time,
#         price, total_seats, class }
# ============================================================
@flights_bp.route('/', methods=['POST'])
@require_auth
@require_admin
def create_flight():
    try:
        data = request.get_json()
        # Trimitem direct la IO Service — validarea e acolo
        from src.services.io_client import IO_URL, INTERNAL_HEADERS
        import requests
        response = requests.post(
            f'{IO_URL}/flights',
            headers=INTERNAL_HEADERS,
            json=data
        )
        response.raise_for_status()
        return jsonify(response.json()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400