import synthesizer
import pytest
import numpy

midi_data = synthesizer.read_midi(
    "/Users/gabrul/Documents/Cosas mías/Code/composer/music/midi_files/bwv988.mid")


synthesizer.get_sound_window(midi_data)
for instrument in midi_data.instruments:
    print(len(instrument.notes))
    for note in instrument.notes:
        print(note.start)
    for change in instrument.control_changes:
        print(change.time)
    for pitch in instrument.pitch_bends:
        print(pitch.time)


def test_synthesize_midi():

    assert numpy.any(synthesizer.synthesize_midi(midi_data))
