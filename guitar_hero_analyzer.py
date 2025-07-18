import pyaudio
import numpy as np
import pygame
import mido
import time
import random
CHUNK = 4096  # Audio chunk size
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
RMS_THRESHOLD = 0.01  # Threshold for detecting silence
BEND_RANGE = 820  # Max pitch bend deviation (approx 0.2 semitones)
FFT_PAD_FACTOR = 2  # Zero-pad FFT to this multiple of CHUNK for better resolution

# Musical notes array
NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
def parabolic(f, x):
    """Quadratic interpolation for estimating the true position of an inter-sample maximum."""
    if x <= 0 or x >= len(f) - 1:
        return x, f[x]
    a, b, c = f[x-1], f[x], f[x+1]
    denom = (a - 2 * b + c)
    if denom == 0:
        return x, b
    vx = x + 0.5 * (a - c) / denom
    vy = b - 0.25 * (a - c)**2 / denom
    return vx, vy
def get_pitch(data):
    """Detect pitch using FFT with windowing, zero-padding, HPS, and parabolic interpolation."""
    if len(data) != CHUNK:
        return 0

    # Apply Hann window to reduce leakage
    window = np.hanning(CHUNK)
    data = data * window

    # Compute zero-padded RFFT for better resolution
    nfft = CHUNK * FFT_PAD_FACTOR
    fft = np.fft.rfft(data, n=nfft)
    mag_spec = np.abs(fft)

    # Basic Harmonic Product Spectrum (HPS) to emphasize fundamental
    hps_spec = np.copy(mag_spec)
    num_harmonics = 3
    for h in range(2, num_harmonics + 1):
        decimated = mag_spec[::h]
        hps_len = len(decimated)
        hps_spec[:hps_len] *= decimated

    # Log-magnitude for peak finding (add epsilon to avoid log(0))
    log_hps = 20 * np.log10(hps_spec + 1e-10)

    # Find peak bin and refine with parabolic interpolation
    peak_bin = np.argmax(log_hps)
    if peak_bin > 0 and peak_bin < len(log_hps) - 1:
        true_bin = parabolic(log_hps, peak_bin)[0]
    else:
        true_bin = peak_bin

    # Convert bin to frequency (limit to audible range, e.g., >20 Hz for guitar low E ~82 Hz)
    freq = true_bin * RATE / nfft
    if freq < 20:
        return 0
    return freq
def freq_to_note_and_num(freq):
    """Convert frequency to note name and MIDI note number."""
    if freq <= 0:
        return None, None
    num = round(69 + 12 * np.log2(freq / 440.0))
    note_name = NOTES[num % 12]
    octave = (num // 12) - 1
    return f"{note_name}{octave}", num
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
pygame.init()
screen = pygame.display.set_mode((600, 200))
pygame.display.set_caption("Guitar Hero MIDI HUD")
font = pygame.font.SysFont(None, 48)
clock = pygame.time.Clock()
# print(mido.get_output_names())  # Uncomment to list ports, then choose one below
midi_out = mido.open_output()  # Default; replace with mido.open_output('Your Port Name') if needed
current_note_num = None
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Read audio data (ignore overflow if callbacks fall behind)
    raw_data = stream.read(CHUNK, exception_on_overflow=False)
    data = np.frombuffer(raw_data, np.float32)

    # Check if there's significant sound
    rms = np.sqrt(np.mean(data ** 2))
    if rms < RMS_THRESHOLD:
        freq = 0
    else:
        freq = get_pitch(data)

    note, note_num = freq_to_note_and_num(freq)

    # Handle note changes
    if note_num != current_note_num:
        if current_note_num is not None:
            midi_out.send(mido.Message('note_off', note=current_note_num, velocity=0))
        if note_num is not None:
            # Apply slight variation with pitch bend
            bend = int(random.uniform(-BEND_RANGE, BEND_RANGE))
            midi_out.send(mido.Message('pitchwheel', pitch=bend))
            midi_out.send(mido.Message('note_on', note=note_num, velocity=64))
        current_note_num = note_num

    # Update HUD
    screen.fill((0, 0, 0))
    if note:
        display_text = f"Detected: {note} | Freq: {freq:.2f} Hz | MIDI Note: {note_num}"
    else:
        display_text = "No note detected"
    text_surface = font.render(display_text, True, (255, 255, 255))
    screen.blit(text_surface, (20, 80))
    pygame.display.flip()

    clock.tick(30)  # Limit to 30 FPS
# Cleanup
if current_note_num is not None:
    midi_out.send(mido.Message('note_off', note=current_note_num, velocity=0))
stream.stop_stream()
stream.close()
p.terminate()
midi_out.close()
pygame.quit()


