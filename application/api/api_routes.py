"""Blueprint to authenticate users."""
import sqlite3
from flask import Blueprint, jsonify, make_response
# from . import lookup

# Set up a blueprint
api_bp = Blueprint("api_bp", __name__)

# Connect to SQLite3 database
conn = sqlite3.connect('book.db', check_same_thread=False)
cursor = conn.cursor()


@api_bp.route("/api/<isbn>")
def api(isbn):
    """Entertain api calls."""
    try:
        # Fetch book info from db
        cursor.execute("""SELECT * FROM books WHERE isbn = ?""", (isbn,))
        book = cursor.fetchone()
        if book:
            # Get rating from Goodread
            # goodread_info = lookup(book["isbn"])
            return jsonify(
                {
                    "title": book[0][2],
                    "author": book[0][3],
                    "year": [0][4],
                    "isbn": [0][1],
                    "review_count": '4',
                    "average_score": '4.7',
                }
            )
        else:
            return make_response(
                jsonify(
                    {
                        "error": {
                            "code": 404,
                            "message": "Book Not Found",
                            "errors": [
                                {
                                    "domain": "Api",
                                    "message": "Book Not Found",
                                }
                            ],
                        }
                    }
                ),
                404,
            )
    except Exception:
        print("api_routes ")
        return make_response(
            jsonify(
                {
                    "error": {
                        "code": 500,
                        "message": "Internal Server Error",
                        "errors": [
                            {
                                "domain": "Api",
                                "message": "Internal Server Error",
                            }
                        ],
                    }
                }
            ),
            500,
        )
