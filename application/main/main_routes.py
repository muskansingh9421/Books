"""Routes for logged in users."""

import sqlite3
from datetime import datetime
from flask import (Blueprint, render_template,
                   session, request, abort, flash, redirect, url_for)


# Set up a blueprint
main_bp = Blueprint("main_bp", __name__,
                    template_folder="templates")


@main_bp.route("/")
def home():
    """Home route."""
    # Check if user is logged in
    if session.get("username") is None:
        return render_template("home.html")

    return render_template("home.html",
                           name=session["username"])


@main_bp.route("/books", methods=["GET"])
def books():
    """All matching books."""

    # User input
    search_term = request.args.get("search")
    try:
        connection = sqlite3.connect('book.db', check_same_thread=False)
        cursor = connection.cursor()
        # cursor.execute("""SELECT * FROM books WHERE id =?""",(3,))
        # results= cursor.fetchall()
        # print("results")
        # print(results)
        results = cursor.execute("""SELECT * FROM books WHERE title LIKE ?
                                OR author LIKE ?
                                OR isbn LIKE ?""",
                             ('%' + search_term.lower() + '%', '%' + search_term.lower() + '%', '%' + search_term.lower() + '%')).fetchall()

        return render_template("books.html",
                               term=search_term,
                               search_term=search_term,
                               results=results)
    except Exception as e:
        print(e)
        abort(500)
    finally:
        cursor.close()
        connection.close()


@main_bp.route("/book/<int:book_id>")
@main_bp.route("/book", defaults={"book_id": None}, methods=["POST"])
def book(book_id):
    """View book."""

    # When user submits a review
    if request.method == "POST":
        rating = request.form.get("rating")
        comment = request.form.get("comment")
        if rating:
            # Submit review
            try:
                connection = sqlite3.connect('book.db')
                cursor = connection.cursor()
                # Insert review into db
                cursor.execute("""INSERT INTO reviews (user_id, book_id, rating, comment, posted_on)
                                VALUES (?, ?, ?, ?, ?)""",
                           (session["user_id"], session["book_id"], rating, comment, datetime.utcnow().date()))
                connection.commit()
                return redirect(url_for('.book', book_id=session["book_id"]))

            except Exception as e:
                print(e)
                abort(500)
            finally:
                cursor.close()
                connection.close()
        else:
            flash("Please give a rating to submit review.")
            return redirect(url_for('.book', book_id=session["book_id"]))

    else:
        # When user visits a book page
        try:
            connection = sqlite3.connect('book.db', check_same_thread=False)
            cursor = connection.cursor()

            # Get all reviews for a book
            cursor.execute("""SELECT rating, comment, posted_on, user_id
                                FROM reviews
                                WHERE book_id = ?
                                """,
                                (book_id,))
            reviews = cursor.fetchall()

            # Check logged in user's past reviews
            past_review = False
            if "user_id" in session:
                # Save book_id to session
                session["book_id"] = book_id
                for review in reviews:
                    if review[3] == session["user_id"]:
                        past_review = True

            # Get book information
            book = cursor.execute("""SELECT * FROM books WHERE id = ?""",
                            (book_id,)).fetchone()
            print(reviews)
            if book:
                return render_template("book.html",
                                    term=book[1],
                                    search_term=book[1],
                                    title=book[1],
                                    author=book[2],
                                    year=book[3],
                                    isbn=book[4],
                                    past_review=past_review,
                                    reviews=reviews)
            else:
                abort(400)

        except Exception as e:
            print("Main_routes")
            print(e)
            abort(500)

    connection.close()