from pathlib import Path

import numpy

from app.backend.synthesizer import read_midi, synthesize_midi

MIDI_FILE = Path(__file__).parents[1] / "music" / "midi_files" / "bwv988.mid"


def test_synthesize_midi():
    midi_data = read_midi(str(MIDI_FILE))
    assert numpy.any(synthesize_midi(midi_data))
