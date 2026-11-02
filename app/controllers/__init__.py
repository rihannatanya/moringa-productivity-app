from flask import Blueprint, jsonify, request, session
from sqlalchemy import or_

from app import db
from app.models import User

auth_bp = Blueprint("auth", __name__)


def request_data():
    return request.get_json(silent=True) or {}


@auth_bp.route("/signup", methods=["POST"])
def signup():

    data = request_data()

    username = str(data.get("username", "")).strip()
    email = str(data.get("email", "")).strip().lower()
    password = data.get("password", "")

    if not username or not email:
        return jsonify({
            "error": "Username and email are required."
        }), 400

    if not isinstance(password, str) or len(password) < 8:
        return jsonify({
            "error": "Password must contain at least 8 characters."
        }), 400

    existing_user = User.query.filter(
        or_(
            User.username == username,
            User.email == email
        )
    ).first()

    if existing_user:
        return jsonify({
            "error": "Username or email already exists."
        }), 409

    user = User(
        username=username,
        email=email
    )

    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    session.clear()
    session["user_id"] = user.id

    return jsonify(user.to_dict()), 201


@auth_bp.route("/login", methods=["POST"])
def login():

    data = request_data()

    identifier = str(
        data.get("username") or data.get("email") or ""
    ).strip()

    password = data.get("password", "")

    if not identifier or not isinstance(password, str):
        return jsonify({
            "error": "Username/email and password are required."
        }), 400

    user = User.query.filter(
        or_(
            User.username == identifier,
            User.email == identifier.lower()
        )
    ).first()

    if user is None or not user.check_password(password):
        return jsonify({
            "error": "Invalid username/email or password."
        }), 401

    session.clear()
    session["user_id"] = user.id

    return jsonify(user.to_dict()), 200


@auth_bp.route("/logout", methods=["DELETE", "POST"])
def logout():

    session.clear()

    return jsonify({
        "message": "Logged out successfully."
    }), 200


@auth_bp.route("/check_session", methods=["GET"])
def check_session():

    user_id = session.get("user_id")

    if not user_id:
        return jsonify({
            "error": "Unauthorized"
        }), 401

    user = db.session.get(User, user_id)

    if user is None:
        session.clear()

        return jsonify({
            "error": "Unauthorized"
        }), 401

    return jsonify(user.to_dict()), 200