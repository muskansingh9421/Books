"""Blueprint to authenticate users."""

from werkzeug.security import check_password_hash, generate_password_hash
from flask import (Blueprint, render_template, request, abort, redirect,
                   url_for, flash, session)

import sqlite3

conn = sqlite3.connect('book.db', check_same_thread=False)
db = conn.cursor()

# Set up a blueprint
auth_bp = Blueprint("auth_bp", __name__,
                    template_folder="templates")


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    """
    User sign-up.

    GET: Serve sign up page.
    POST: Register user and redirect to homepage.
    """

    # When user submits the signup form
    if request.method == "POST":

        # Grab form data
        username = request.form.get("username")
        password = request.form.get("password")

        # Input validation
        if not username:
            flash("Please provide a username.")
            return redirect(url_for(".signup"))
        if not password:
            flash("Please provide a password.")
            return redirect(url_for(".signup"))

        # Check if username already registered
        db.execute("""SELECT id FROM users WHERE username = ?""",
                   (username,))
        username_exists = db.fetchone()
        print(username_exists)
        if username_exists:
            flash("Username alreay exists!")
            return redirect(url_for('.signup'))

        # Register user
        try:
            db.execute("""INSERT INTO users(username, password) VALUES(?, ?)""",
                       (username, generate_password_hash(password)))
            conn.commit()
            user_id = db.lastrowid

            # Log in user
            session["username"] = username
            session["user_id"] = user_id
            return redirect(url_for('main_bp.home'))
        except Exception as e:
            print("auth_routes signup")
            print(e)
            abort(500)

    # When user visits the signup page
    return render_template("signup.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Login user.

    GET: Serve login page.
    POST: If password mathces, log user in.
    """

    # When user submits the login form
    if request.method == "POST":

        # Grab form data
        username = request.form.get("username")
        password = request.form.get("password")

        # Input validation
        if not username:
            flash("Please provide a username.")
            return redirect(url_for(".login"))
        if not password:
            flash("Please provide a password.")
            return redirect(url_for(".login"))

        # Check user
        db.execute("""SELECT * FROM users WHERE username = ?""",
                   (username,))
        user = db.fetchone()
        if not user:
            flash("Invalid username/password!")
            return redirect(url_for('.login'))

        # Log in user
        if check_password_hash(user[2], password):
            session["username"] = username
            session["user_id"] = user[0]
            flash("Welcome, " + session["username"])
            return redirect(url_for('main_bp.home'))

        flash("Invalid username/password!")
        return redirect(url_for('.login'))

    # When user visits the login page
    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    """Logout user by clearing session."""
    session.clear()
    return redirect(url_for("main_bp.home"))
