# Conversation log — Playing audio from a MIDI file with `pretty_midi`

**Date:** 2026-08-16
**Context:** Python, `pretty_midi`, MIDI → audio playback
**Reference open during conversation:** [pretty_midi Tutorial.ipynb](https://nbviewer.org/github/craffel/pretty-midi/blob/main/Tutorial.ipynb)

---

## Q1 — Which method plays the synthesizer's sound?

**User:**

> I'm trying to figure out how to play sound from a MIDI file. I already have this code, but I'm not sure about what method I should call to play the actual sound of the synthesizer:

```python
import pretty_midi


def main():

    midi_data = pretty_midi.PrettyMIDI("midi_files/bwv772.mid")
    audio_data = midi_data.synthesize()



if __name__ == "__main__":
    main()
```

**Assistant:**

There isn't one — `pretty_midi` has no playback. `synthesize()` already did its job: it returns a NumPy array of audio samples (a sine-wave rendering, default `fs=44100`). Playing that array is a separate library's job.

Simplest option, `sounddevice`:

```python
import pretty_midi
import sounddevice as sd


def main():
    midi_data = pretty_midi.PrettyMIDI("midi_files/bwv772.mid")
    fs = 44100
    audio_data = midi_data.synthesize(fs=fs)

    sd.play(audio_data, samplerate=fs)
    sd.wait()  # block until playback finishes


if __name__ == "__main__":
    main()
```

(`pip install sounddevice` — it needs PortAudio, which ships with the wheel on most platforms.)

Two things worth knowing:

**It'll sound like a bad organ.** `synthesize()` renders every note as a plain sine wave. If you want it to sound like an actual instrument, use `midi_data.fluidsynth(fs=fs)` instead, which renders through a SoundFont — needs `pyfluidsynth` plus a `.sf2` file (pass `sf2_path=...`, or it looks for a default). Same deal: it returns an array, doesn't play it.

**If you'd rather write a file than play live:**

```python
from scipy.io.wavfile import write
import numpy as np

write("out.wav", fs, (audio_data / np.max(np.abs(audio_data)) * 32767).astype(np.int16))
```

And in a Jupyter notebook, the usual move is `IPython.display.Audio(audio_data, rate=fs)` — that gives you a play widget inline.

---

## Q2 — What does `fs` stand for?

**Assistant:**

Sampling frequency — the sample rate, in Hz. It's how many audio samples per second are used to represent the waveform.

`fs=44100` means 44,100 samples per second (CD quality). So a 10-second piece gives you an array of 441,000 floats.

The key thing is that the number is meaningless on its own — it has to match between rendering and playback. If you synthesize at 44100 but tell `sd.play` the rate is 22050, it plays back at half speed, an octave lower. That's why the same `fs` variable is passed to both in the example.

Common values: 44100 (CD), 48000 (video/pro audio), 22050 (lower quality, half the data). Higher rates capture higher frequencies, at the cost of bigger arrays.

---

## Q3 — What purpose does `wait()` serve?

**Assistant:**

`sd.play()` doesn't play the sound — it *starts* playing it and returns immediately.

Under the hood, sounddevice hands your array to PortAudio, which opens an audio stream and spins up a background thread. That thread periodically calls back into your process asking "give me the next chunk of samples," and sounddevice feeds it slices of your array. Your Python code, meanwhile, has already moved on to the next line.

So without `wait()`:

```python
sd.play(audio_data, samplerate=fs)
# main() returns here, ~instantly
# __main__ block ends, interpreter starts shutting down
# the audio stream gets torn down mid-playback
```

You'd hear a click, a few milliseconds of sound, or nothing at all, depending on timing. The script exits before the background thread has done any real work.

`sd.wait()` blocks the main thread until the stream reports it's finished — that's it. It's purely "don't let this program end (or move on) yet."

Two consequences worth noting:

**The gap between them is usable.** Because `play` is non-blocking, anything you put between the two lines runs *while* audio plays:

```python
sd.play(audio_data, samplerate=fs)
print("Now playing:", len(audio_data) / fs, "seconds")
do_something_else()
sd.wait()
```

That's the whole reason for the split API. If you don't need that, `sd.play(audio_data, samplerate=fs, blocking=True)` does both in one call.

**Ctrl+C during `wait()` is how you stop early** — or `sd.stop()` from another thread. While blocked in `wait()`, the main thread isn't doing anything else, so interrupting is clean.

This asynchronous pattern is standard for audio libraries generally, not a sounddevice quirk — playback has to happen on a real-time thread with tight timing guarantees, which is incompatible with running inside your regular interpreter flow.

---

## Summary of key points

- `pretty_midi` synthesizes audio but never plays it; `synthesize()` and `fluidsynth()` both return NumPy arrays.
- `synthesize()` = sine waves (thin sound). `fluidsynth(sf2_path=...)` = SoundFont rendering (realistic instruments, needs `pyfluidsynth`).
- `fs` = sampling frequency in Hz; must match between synthesis and playback or pitch/speed will be wrong.
- Playback requires a separate library: `sounddevice` (live), `scipy.io.wavfile.write` (to file), or `IPython.display.Audio` (notebook).
- `sd.play()` is non-blocking; `sd.wait()` blocks until playback completes so the process doesn't exit early. `blocking=True` combines the two.
