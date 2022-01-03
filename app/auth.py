import functools
from os import error
import sqlite3
from flask import (Blueprint, app, flash, g, redirect,
                   render_template, request, session, url_for)
from werkzeug import security
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if session != {}:
        @bp.route('/logout')
        def logout():
            session.clear()
        logout()
    if request.method == "POST":
        username = request.form["username"].capitalize()
        password = request.form["password"]
        security_question = request.form["security-question"]
        db = get_db()
        error = None

        if not username:
            error = "Username is required"
        elif not password:
            error = "Password is required"
        elif not security_question:
            error = "Please answer the security question"

        elif db.execute('SELECT id FROM user WHERE username = ?', (username,)).fetchone() is not None:
            error = f"{username} is already registered"

        if error is None:
            db.execute('INSERT INTO user (username, password, security_question) VALUES (?, ?, ?)',
                       (username, generate_password_hash(password), security_question))
            db.commit()

            return redirect(url_for('auth.login'))
        else:
            flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if session != {}:
        @bp.route('/logout')
        def logout():
            session.clear()
            return redirect(url_for('auth.login'))
        logout()
    if request.method == 'POST':
        username = request.form['username'].capitalize()
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
         'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None or not check_password_hash(user['password'], password):
            error = 'Incorrect username or password'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('calendar.day_view'))

        flash(error)

    return render_template('auth/login.html')


@bp.route('/reset-password', methods=('GET', 'POST'))
def security_question():
    if request.method == 'POST':
        username = request.form['username']
        security_ans = request.form['security-question']
        new_password = request.form['new-password']
        confirm_password = request.form['confirm']
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)).fetchone()

        if user is None or security_ans != user['security_question']:
            error = "Username not found or the answer is wrong"

        if error is None:
            if new_password == confirm_password:
                new_hashed_password = generate_password_hash(new_password)
                db.execute(f"UPDATE user SET password = ? WHERE username = ? AND security_question = ?",
                           (new_hashed_password, username, security_ans))
                db.commit()
                return redirect(url_for('auth.login'))
            else:
                error = "The 2 different passwords don't match"

        else:
            flash(error)

    return render_template('auth/reset-password.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/delete-account', methods=("GET", 'POST'))
def delete_account():
    if request.method == "POST":
        id = session['user_id']
        password = request.form['password']
        security_ans = request.form['security-question']
        error = None
        db = get_db()
        user = db.execute("SELECT * FROM user WHERE id = ?", (id,)).fetchone()
        if security_ans == user['security_question'] and check_password_hash(user['password'], password):
            db.execute('DELETE FROM post WHERE author_id = ?', (id,))
            db.commit()
            db.execute('DELETE FROM user WHERE id = ?', (id,))
            db.commit()

            @bp.route('/logout')
            def logout():
                session.clear()
                return redirect(url_for('auth.login'))
            logout()
        elif security_ans == user['security_question']:
            error = "Incorrect password"
        elif password == user['password']:
            error = "Incorrect answer"

        else:
           error = "Incorrect password or answer"
        flash(error)
    return render_template('auth/delete.html')
