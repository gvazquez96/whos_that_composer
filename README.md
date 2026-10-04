# Who's That Composer?

A small Flask web game for guessing classical music. Each round plays a short clip synthesized from a MIDI file, and you pick the right answer from four options. The interface is in Spanish.

## Features

- **Three game modes:** guess the piece, the composer, or the year of composition.
- **Lives and wildcards:** 2 lives per game, a 50-50 wildcard and a "+30 secs" wildcard that replays a longer clip.
- **User accounts:** register and log in (passwords hashed with bcrypt); your best streak is saved.
- **71 pieces** from Bach to Rachmaninoff, defined in `app/pieces.csv`.

## Requirements

- Python 3.12+
- The packages in `requirements.txt` (Flask, Flask-SQLAlchemy, Flask-Session, pretty-midi, numpy, scipy, bcrypt…)

## Getting started

```bash
git clone https://github.com/gvazquez96/whos_that_composer.git
cd whos_that_composer
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

The app starts at <http://127.0.0.1:5000> and opens your browser automatically. The SQLite database (`instance/site.db`) is created on first run.

## Project structure

```
run.py                 Entry point
app/
├── __init__.py        App factory (Flask, sessions, database)
├── models.py          User model
├── pieces.csv         Piece catalogue (name, year, catalogue no., composer, MIDI file)
├── backend/           Piece picking, answer options and MIDI-to-WAV synthesis
├── routes/            Blueprints: index, auth, game loop
├── music/midi_files/  MIDI files + CREDITS.md
├── templates/         Jinja2 templates
└── static/            CSS, images, GIFs and sounds
```

## Adding pieces

1. Drop the `.mid` file into `app/music/midi_files/`.
2. Add a row to `app/pieces.csv` with `piece_name,year,catalogue,composer,midi_file`.

## Credits

The compositions are in the public domain; the MIDI sequences belong to their respective authors and are used for non-commercial, educational purposes only. See [`app/music/midi_files/CREDITS.md`](app/music/midi_files/CREDITS.md) for sources.
