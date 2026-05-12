import os
import requests

# URL-ul IO Service — citit din variabila de mediu
IO_URL = os.getenv('IO_SERVICE_URL', 'http://io-service:3002')

# Headerul de autentificare inter-servicii
# Același secret pe care îl verifică serviceAuth din IO Service
INTERNAL_HEADERS = {
    'x-internal-secret': os.getenv('INTERNAL_SECRET'),
    'Content-Type': 'application/json'
}

def get_flights(params=None):
    """Caută zboruri cu filtre opționale (origin, destination, class, date)"""
    response = requests.get(
        f'{IO_URL}/flights',
        headers=INTERNAL_HEADERS,
        params=params  # trimite query params: ?origin=OTP&destination=LHR
    )
    response.raise_for_status()
    return response.json()

def get_flight(flight_id):
    """Returnează detaliile unui zbor după ID"""
    response = requests.get(
        f'{IO_URL}/flights/{flight_id}',
        headers=INTERNAL_HEADERS
    )
    response.raise_for_status()
    return response.json()

def get_user_reservations(user_id):
    """Returnează toate rezervările unui user"""
    response = requests.get(
        f'{IO_URL}/reservations/user/{user_id}',
        headers=INTERNAL_HEADERS
    )
    response.raise_for_status()
    return response.json()

def get_reservation(reservation_id):
    """Returnează o rezervare după ID"""
    response = requests.get(
        f'{IO_URL}/reservations/{reservation_id}',
        headers=INTERNAL_HEADERS
    )
    response.raise_for_status()
    return response.json()

def create_reservation(user_id, flight_id, passengers):
    """Creează o rezervare nouă"""
    response = requests.post(
        f'{IO_URL}/reservations',
        headers=INTERNAL_HEADERS,
        json={
            'user_id': user_id,
            'flight_id': flight_id,
            'passengers': passengers
        }
    )
    response.raise_for_status()
    return response.json()

def cancel_reservation(reservation_id):
    """Anulează o rezervare"""
    response = requests.patch(
        f'{IO_URL}/reservations/{reservation_id}',
        headers=INTERNAL_HEADERS,
        json={'status': 'cancelled'}
    )
    response.raise_for_status()
    return response.json()