import os
import jwt
from functools import wraps
from flask import request, jsonify

JWT_SECRET = os.getenv('JWT_SECRET')

def require_auth(f):
    """
    Decorator aplicat pe rutele protejate.
    Verifică headerul Authorization: Bearer <token>
    Dacă token-ul e valid, pune payload-ul în request.user
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'No token provided'}), 401

        token = auth_header.split(' ')[1]  # extragem după "Bearer "

        try:
            # decodăm și verificăm token-ul
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            request.user = payload  # punem payload-ul pe request
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 403

        return f(*args, **kwargs)
    return decorated

def require_admin(f):
    """
    Decorator pentru rutele de admin.
    Se aplică DUPĂ require_auth.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if not hasattr(request, 'user') or request.user.get('role') != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated