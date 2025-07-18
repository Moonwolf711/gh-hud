# gh-hud

This repository contains a small MIDI HUD experiment. The main script
`guitar_hero_analyzer.py` listens to your microphone, detects the
fundamental frequency and sends MIDI messages to the selected output
port while displaying the note on screen.

## Requirements

Install the following Python packages before running the analyzer:

- numpy
- pygame
- mido
- PyAudio

They can be installed with pip:

```bash
pip install numpy pygame mido PyAudio
```

PyAudio may require additional system packages such as the PortAudio
libraries. Refer to your platform's instructions if the installation fails.

## Running the analyzer

After installing the dependencies, run:

```bash
python guitar_hero_analyzer.py
```

A small window opens showing the detected note and frequency. MIDI
`note_on`/`note_off` messages are sent for the active note along with a
subtle pitch bend.

## MIDI output notes

The script opens the default MIDI output returned by `mido`. If you have
multiple ports, call `mido.get_output_names()` to list them and replace
`mido.open_output()` with `mido.open_output('Your Port Name')`.

Any hardware or virtual MIDI device capable of receiving these messages
can be used. On systems without physical MIDI hardware you can use a
virtual loopback port (e.g. LoopMIDI on Windows or a2jmidid/virtual
MIDI on Linux) to route the messages to a synthesizer or DAW.
