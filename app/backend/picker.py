import csv
import random
from pathlib import Path
from app.backend.classes import Composer, Piece


def picker(pieces):
    """
    Randomly picks a piece from set created by load_composers()
    """

    used = pieces
    piece = random.choice(list(used))
    used.remove(piece)
    return piece


def load_composers():
    """
    loads all composer and piece classes into memory
    """

    composers = {}
    pieces = set()

    # --> opens csv containing metadata
    with open(Path(__file__).parents[1] / "pieces.csv", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        # --> iterates over csv and creates composer objects (if not already existing).
        # --> Then creates one Piece object for each piece whose composer header matches the Composer.name,
        # -->  and adds the piece to the composer's.pieces set
        # --> and adds the piece object to a set of pieces
        # --> then returns both the composers dict and the pieces set
        for row in reader:
            if row["composer"] not in composers:
                composer = Composer(row["composer"])
                composers.update({row["composer"]: composer})
            composer = composers[row["composer"]]
            piece = Piece(
                composer, row["piece_name"], row["year"], row["catalogue"], row["midi_file"])
            composer.add_piece(piece)
            pieces.add(piece)
    return composers, pieces
