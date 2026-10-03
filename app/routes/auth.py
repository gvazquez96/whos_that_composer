from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError, NoResultFound
from app.models import db, User
import bcrypt

auth_bp = Blueprint("auth", __name__, template_folder="../templates")


@auth_bp.route("/register", methods=["POST", "GET"])
def register():
    """ PULLS UP REGISTER PAGE """
    return render_template("register.html")


@auth_bp.route("/login", methods=["POST", "GET"])
def login():
    """ CHECKS IF USER IS ALREADY LOGGED IN. IF NOT, RENDERS LOGIN PAGE """
    if session.get("user") is not None:
        flash("Ya has iniciado sesión")
        return redirect(url_for("index.index"))
    else:
        return render_template("login.html")


@auth_bp.route("/logout", methods=["POST", "GET"])
def logout():
    """ CHECKS IF USER IS ALREADY LOGGED OUT. IF NOT, RENDERS LOGOUT PAGE """
    if "user" not in session:
        flash("Ya has cerrado sesión")
        return redirect(url_for("index.index"))
    else:
        return render_template("logout.html")


@auth_bp.route("/add_user", methods=["POST"])
def add_user():
    """ ADDS USER TO DATABASE """
    user = request.form.get("user").lower()
    password = request.form.get("password")
    if user != "" and password != "":
        to_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(to_bytes, salt)
        try:
            profile = User(name=user, password=hashed, max_streak=0)
            db.session.add(profile)
            db.session.commit()
            flash("Te has registrado correctamente")
            return redirect(url_for("index.index"))
        except IntegrityError:
            flash("Nombre de usuario no disponible. Escoge otro.")
            return redirect(url_for("auth.register"))
    else:
        flash("Es necesario rellenar todos los campos")
        return redirect(url_for("auth.register"))


@auth_bp.route("/remove_user", methods=["GET", "POST"])
def remove_user():
    """ REMOVES USER DATA FROM SESSION """
    if "user" in session:
        session.pop("user")
        session.pop("max_streak")
    if "streak" in session:
        session.pop("streak")
    flash("Sesión restaurada. Inicia sesión para empezar")
    return redirect(url_for("index.index"))


@auth_bp.route("/validate_user", methods=["POST"])
def validate_user():
    """ If user is not in database, redirects to register page. Else, validates password and username """
    name = request.form["user"].lower()
    password = request.form["password"]
    to_bytes = password.encode("utf-8")
    try:
        user = db.session.execute(
            db.select(User).filter_by(name=name)).scalar_one()
        print(user.password)
        if user.name == name and bcrypt.checkpw(to_bytes, user.password):
            session["user"] = user.name
            session["max_streak"] = user.max_streak
            flash(f"Bienvenido, {user.name.capitalize()}")
            return redirect(url_for("index.index"))
        else:
            flash("Usuario o contraseña incorrecta")
            return redirect(url_for("auth.login"))
    except NoResultFound:
        flash("No estás registrado")
        return redirect(url_for("index.index"))


@auth_bp.route("/delete_user", methods=["GET"])
def delete_user():
    """ DELETES USER FROM DB """
    try:
        name = session["user"]
    except KeyError:
        flash("No has iniciado sesión")
        return redirect(url_for("index.index"))
    try:
        user = db.session.execute(
            db.select(User).filter_by(name=name)).scalar_one()
        db.session.delete(user)
        db.session.commit()
        flash("Cuenta borrada con éxito")
        return redirect(url_for("auth.remove_user"))
    except NoResultFound:
        flash("Esta cuenta no existe")
        return redirect(url_for("index.index"))
