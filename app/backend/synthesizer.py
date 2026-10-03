from pretty_midi import PrettyMIDI
from pathlib import Path
import numpy
import scipy
import sounddevice as sd

WINDOW = 10
FS = 44100


def read_midi(prompt: str) -> PrettyMIDI:

    # --> load MIDI into memory (investigar pathlibd para construir rutas de forma portable. La actual implementación solo funciona en Mac)
    midi_data = PrettyMIDI(prompt)
    midi_data.remove_invalid_notes()
    # --> remove possible invalid values
    return midi_data


def get_sound_window(midi: PrettyMIDI, window: int = WINDOW) -> None:
    """
    MUTATES MIDI OBJECT TO CONTAIN NOTES THAT FALL WITHIN SOUND WINDOW. RETURNS NONE.
    """

    # --> gets the start (in seconds) of the first actual sounding note
    beg = midi.get_onsets()[0]

    # --> end equals how many seconds the notes should be sounding
    end = beg + window

    # --> parse instruments list, and within that parse notes list to find notes that fall within WINDOW, and reassign them to the PrettyMIDI object.
    for instrument in midi.instruments:
        notes = []
        changes = []
        pitches = []
        for note in instrument.notes:
            if note.start < end and note.end <= end:
                note.start -= beg
                note.end -= beg
                notes.append(note)
            elif note.start < end and note.end > end:
                note.start -= beg
                note.end = window
                notes.append(note)
        instrument.notes = notes

        # Adds an additional checker to prevent negative times in ControlChange and PitchBend instances
        for change in instrument.control_changes:
            if change.time <= end and change.time - beg >= 0:
                change.time -= beg
                changes.append(change)
        instrument.control_changes = changes

        for pitch in instrument.pitch_bends:
            if pitch.time <= end and pitch.time - beg >= 0:
                pitch.time -= beg
                pitches.append(pitch)
        instrument.pitch_bends = pitches


def synthesize_midi(midi: PrettyMIDI, fs: int = FS) -> numpy.ndarray:

    return midi.synthesize(fs) * 32767


def midi_to_wav(synthesized_midi: numpy.ndarray) -> None:
    int_audio = synthesized_midi.astype(numpy.int16)
    scipy.io.wavfile.write(Path(__file__).parents[1] / "static" /
                           "piece.wav", 44100, int_audio)
