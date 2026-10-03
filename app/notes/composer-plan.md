# Classical Music Bandle (CLI Edition)

A command-line guessing game built in Python. Players listen to a classical music piece starting with just one instrument. If they guess incorrectly, another instrument is unmuted and layered into the audio until the full orchestra is playing.

## 🏗️ Project Architecture

The backend is divided into four distinct modules to keep the code clean and manageable.

### 1. The Data Manager (`data_manager.py`)
Acts as the game's library.
* **Role:** Manages the catalog of available songs and their correct answers.
* **Mechanic:** Loads a dictionary (or JSON file) containing the MIDI filepaths, composers, and acceptable answer variations. Randomly selects the piece for the current game session.

### 2. The MIDI Mixer (`midi_mixer.py`)
The core mechanic of the game.
* **Role:** Acts as a digital mixing board for the MIDI files.
* **Mechanic:** Uses the `pretty_midi` library to read the tracks inside a MIDI file. Based on the current turn number, it isolates the specific tracks (e.g., Turn 1 = Cello only; Turn 2 = Cello + Viola) and exports a temporary MIDI file (`current_clue.mid`).

### 3. The Audio Engine (`audio_engine.py`)
The bridge between MIDI data and audible sound.
* **Role:** Converts the isolated MIDI tracks into a playable audio format and handles playback.
* **Mechanic:** 
  1. Calls **FluidSynth** (via a library like `midi2audio`) and uses a SoundFont (`.sf2` file) to render `current_clue.mid` into `output.wav`.
  2. Uses an audio playback library (like `pygame` or `simpleaudio`) to play the WAV file out loud in the terminal.

### 4. The Game Loop (`main.py`)
The central controller and user interface.
* **Role:** Manages the game flow, turn counters, and user input.
* **Mechanic:** Runs a `while` loop that prompts the user for a guess, checks the answer against the Data Manager, and instructs the MIDI Mixer to add another instrument if the guess is incorrect.

---

## 🛠️ Prerequisites & Tools Needed

To build this, you will need to install a few external tools and Python libraries:

**System Requirements:**
* **FluidSynth:** A command-line synthesizer (requires installation on your OS via Homebrew/apt/etc.)
* **A SoundFont (.sf2):** A free library of instrument sounds (e.g., *FluidR3_GM.sf2*) so the MIDI files sound like real instruments.

**Python Libraries:**
* `pretty_midi` (for editing the MIDI files)
* `midi2audio` (for talking to FluidSynth)
* `pygame` or `simpleaudio` (for playing the WAV file)

---

## 📂 Suggested Folder Structure

```text
classical_bandle/
│
├── main.py                 # The game loop
├── data_manager.py         # Library logic
├── midi_mixer.py           # MIDI processing logic
├── audio_engine.py         # Audio conversion & playback
│
├── data/
│   ├── songs.json          # List of answers and filepaths
│   └── midi_files/         # Raw .mid files (e.g., beethoven_5.mid)
│
├── assets/
│   └── soundfont.sf2       # The instrument sounds for FluidSynth
│
├── temp/                   # Folder for generated files (clue.mid, output.wav)
│
└── README.md


features a implementar: 

- comodines: escucha 20 segundos en vez de 10, por ejemplo, o deja solo dos opciones posibles. cada 10 acertadas, se gana un comodín aleatorio. 