from flask import Blueprint, request, jsonify
from src.middleware.auth import require_auth
from src.services import io_client

reservations_bp = Blueprint('reservations', __name__)

# ============================================================
# GET /reservations
# Rezervările userului autentificat curent
# Header: Authorization: Bearer <token>
# ============================================================
@reservations_bp.route('/', methods=['GET'])
@require_auth
def get_my_reservations():
    try:
        # user_id vine din payload-ul JWT decodat de require_auth
        user_id = request.user['userId']
        reservations = io_client.get_user_reservations(user_id)
        return jsonify(reservations)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================
# GET /reservations/:id
# Detalii rezervare — userul poate vedea doar rezervările lui
# ============================================================
@reservations_bp.route('/<int:reservation_id>', methods=['GET'])
@require_auth
def get_reservation(reservation_id):
    try:
        reservation = io_client.get_reservation(reservation_id)

        # Verificăm că rezervarea aparține userului curent
        if reservation['user_id'] != request.user['userId']:
            return jsonify({'error': 'Forbidden'}), 403

        return jsonify(reservation)
    except Exception as e:
        return jsonify({'error': str(e)}), 404


# ============================================================
# POST /reservations
# Creează o rezervare nouă
# Header: Authorization: Bearer <token>
# Body: { flight_id, passengers }
# ============================================================
@reservations_bp.route('/', methods=['POST'])
@require_auth
def create_reservation():
    try:
        data = request.get_json()
        flight_id  = data.get('flight_id')
        passengers = data.get('passengers', 1)

        if not flight_id:
            return jsonify({'error': 'flight_id is required'}), 400

        # user_id vine din JWT — userul nu îl poate falsifica
        user_id = request.user['userId']

        reservation = io_client.create_reservation(user_id, flight_id, passengers)
        return jsonify(reservation), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


# ============================================================
# PATCH /reservations/:id/cancel
# Anulează o rezervare
# Header: Authorization: Bearer <token>
# ============================================================
@reservations_bp.route('/<int:reservation_id>/cancel', methods=['PATCH'])
@require_auth
def cancel_reservation(reservation_id):
    try:
        # Verificăm că rezervarea aparține userului curent
        reservation = io_client.get_reservation(reservation_id)
        if reservation['user_id'] != request.user['userId']:
            return jsonify({'error': 'Forbidden'}), 403

        if reservation['status'] == 'cancelled':
            return jsonify({'error': 'Reservation already cancelled'}), 400

        updated = io_client.cancel_reservation(reservation_id)
        return jsonify(updated)
    except Exception as e:
        return jsonify({'error': str(e)}), 400