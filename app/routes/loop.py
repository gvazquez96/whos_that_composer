import random
from flask import session, redirect, url_for, Blueprint, render_template, request, flash
from app.models import db, User
from app.backend.synthesizer import get_sound_window, synthesize_midi, midi_to_wav, read_midi
from app.backend.picker import picker, load_composers
from app.backend.answers import wrong_answers, options_table
from pathlib import Path

loop_bp = Blueprint("loop", __name__, template_folder="../templates")

_, pieces = load_composers()


@loop_bp.route("/gamemode")
def gamemode():
    return render_template("gamemode.html")


@loop_bp.route("/new_game")
def new_game():
    """ STARTS A NEW GAME """
    if "user" not in session:
        flash("Tienes que iniciar sesión")
        return redirect(url_for("index.index"))
    session["streak"] = 0
    session["wildcards"] = {
        "fifty_fifty": "50-50",
        "thirty_secs": "+30 secs"
    }
    session["lives"] = 2
    session["pieces_left"] = pieces
    return redirect(url_for("loop.gamemode"))


@loop_bp.route("/new_round", methods=["GET", "POST"])
def new_round():
    """ STARTS A NEW ROUND """
    if request.method == "POST":
        session["gamemode"] = request.form["gamemode"]
    if session["pieces_left"] == set():
        _, session["pieces_left"] = load_composers()
    piece = picker(session["pieces_left"])
    session["piece"] = piece
    session["correct"] = str(getattr(piece, session["gamemode"]))
    midi = read_midi(Path(__file__).parents[1] / "music" /
                     "midi_files" / piece.midi)
    get_sound_window(midi)
    synth_midi = synthesize_midi(midi)
    midi_to_wav(synth_midi)
    wrong_options = wrong_answers(
        piece, pieces, session["gamemode"])
    options = options_table(session["correct"], wrong_options)
    session["fifty_fifty"] = options_table(session["correct"],
                                           random.sample(wrong_options, 1))
    session["options"] = options
    return redirect(url_for("loop.attempt"))


@loop_bp.route("/end_game/")
def end_game():
    old_streak = session["max_streak"]
    if session["streak"] > session["max_streak"]:
        user = db.session.execute(db.select(User).filter_by(
            name=session["user"])).scalar_one()
        user.max_streak = session.get("streak")
        db.session.commit()
        session["max_streak"] = session.get("streak")
    return render_template("lost.html", piece=session["piece"], gamemode=session["gamemode"], streak=session["streak"],
                           max_streak=old_streak)


@loop_bp.route("/check/", methods=["POST"])
def check():
    """ CHECKS USER INPUT AGAINST CORRECT ANSWER """
    try:
        answer = request.form["answer"]
    except KeyError:
        flash("No olvides seleccionar una respuesta")
        return redirect(url_for("loop.attempt"))
    lives = session["lives"]
    if answer == session["correct"]:
        session["streak"] += 1
        return render_template("correct.html", piece=session["piece"], gamemode=session["gamemode"])
    elif answer != session["correct"] and lives > 1:
        lives -= 1
        session["lives"] = lives
        return render_template("incorrect.html", lives=lives)
    else:
        return end_game()


@loop_bp.route("/attempt")
def attempt():
    """ ALLOWS FOR ANOTHER ATTEMPT IF USER ANSWERS INCORRECTLY AND STILL HAS LIVES LEFT """
    return render_template("question.html", session_options=session["options"],
                           streak=f"{session["streak"]:01d}", max_streak=session["max_streak"],
                           wildcards=session["wildcards"], gamemode=session["gamemode"])


@loop_bp.route("/wildcards/<wildcard>/")
def wildcards(wildcard):
    try:
        session["wildcards"].pop(wildcard)
    except KeyError:
        return redirect(url_for("loop.attempt"))
    if wildcard == "fifty_fifty":
        session["options"] = session["fifty_fifty"]
    else:
        midi = read_midi(Path(__file__).parents[1] / "music" /
                         "midi_files" / session["piece"].midi)
        get_sound_window(midi, 30)
        synth_midi = synthesize_midi(midi)
        midi_to_wav(synth_midi)
    return redirect(url_for("loop.attempt"))
