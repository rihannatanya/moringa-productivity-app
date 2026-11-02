from functools import wraps

from flask import Blueprint, jsonify, request, session

from app import db
from app.models import Note, User

notes_bp = Blueprint("notes", __name__)


def login_required(view):

    @wraps(view)
    def wrapped(*args, **kwargs):

        user_id = session.get("user_id")

        if not user_id or db.session.get(User, user_id) is None:
            return jsonify({
                "error": "Authentication required."
            }), 401

        return view(*args, **kwargs)

    return wrapped


def validated_note_data(data, partial=False):

    if not isinstance(data, dict):
        return None, "A JSON object is required."

    allowed = {
        "title",
        "content",
        "category",
        "is_completed"
    }

    unknown = set(data) - allowed

    if unknown:
        return None, "Unknown fields: " + ", ".join(sorted(unknown))

    cleaned = {}

    if "title" in data:

        title = data["title"]

        if (
            not isinstance(title, str)
            or not title.strip()
            or len(title.strip()) > 150
        ):
            return None, "Invalid title."

        cleaned["title"] = title.strip()

    elif not partial:
        return None, "Title is required."

    if "content" in data:

        if not isinstance(data["content"], str):
            return None, "Content must be a string."

        cleaned["content"] = data["content"]

    if "category" in data:

        if (
            not isinstance(data["category"], str)
            or not data["category"].strip()
        ):
            return None, "Invalid category."

        cleaned["category"] = data["category"].strip()

    if "is_completed" in data:

        if not isinstance(data["is_completed"], bool):
            return None, "is_completed must be true or false."

        cleaned["is_completed"] = data["is_completed"]

    return cleaned, None


# READ ALL NOTES WITH PAGINATION

@notes_bp.route("/notes", methods=["GET"])
@login_required
def index_notes():

    user_id = session["user_id"]

    try:
        page = max(int(request.args.get("page", 1)), 1)
        per_page = min(
            max(int(request.args.get("per_page", 10)), 1),
            100
        )

    except ValueError:
        return jsonify({
            "error": "page and per_page must be integers."
        }), 400

    pagination = (
        Note.query
        .filter_by(user_id=user_id)
        .order_by(Note.created_at.desc())
        .paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
    )

    return jsonify({
        "notes": [
            note.to_dict()
            for note in pagination.items
        ],
        "pagination": {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total,
            "pages": pagination.pages,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev
        }
    }), 200


# CREATE A NOTE

@notes_bp.route("/notes", methods=["POST"])
@login_required
def create_note():

    data, error = validated_note_data(
        request.get_json(silent=True)
    )

    if error:
        return jsonify({"error": error}), 400

    note = Note(
        user_id=session["user_id"],
        **data
    )

    db.session.add(note)
    db.session.commit()

    return jsonify(note.to_dict()), 201


# READ ONE NOTE

@notes_bp.route("/notes/<int:note_id>", methods=["GET"])
@login_required
def show_note(note_id):

    note = Note.query.filter_by(
        id=note_id,
        user_id=session["user_id"]
    ).first()

    if note is None:
        return jsonify({
            "error": "Note not found."
        }), 404

    return jsonify(note.to_dict()), 200


# UPDATE A NOTE

@notes_bp.route(
    "/notes/<int:note_id>",
    methods=["PATCH", "PUT"]
)
@login_required
def update_note(note_id):

    note = Note.query.filter_by(
        id=note_id,
        user_id=session["user_id"]
    ).first()

    if note is None:
        return jsonify({
            "error": "Note not found."
        }), 404

    data, error = validated_note_data(
        request.get_json(silent=True),
        partial=True
    )

    if error:
        return jsonify({"error": error}), 400

    if not data:
        return jsonify({
            "error": "Provide at least one field to update."
        }), 400

    for key, value in data.items():
        setattr(note, key, value)

    db.session.commit()

    return jsonify(note.to_dict()), 200


# DELETE A NOTE

@notes_bp.route(
    "/notes/<int:note_id>",
    methods=["DELETE"]
)
@login_required
def delete_note(note_id):

    note = Note.query.filter_by(
        id=note_id,
        user_id=session["user_id"]
    ).first()

    if note is None:
        return jsonify({
            "error": "Note not found."
        }), 404

    db.session.delete(note)
    db.session.commit()

    return jsonify({
        "message": "Note deleted successfully."
    }), 200