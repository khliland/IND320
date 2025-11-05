# --- Streamlit app to record audio and display STFT spectrogram ---
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import stft

# --- Record audio in browser ---
audio_bytes = st.audio_input("Record your audio", key="audio_recorder")

# --- If no recording, show info message ---
if audio_bytes is None:
    st.info("Please record some audio to see the spectrogram.")
#    st.stop()

# --- Read audio bytes into numpy array ---
else:
    import io
    from scipy.io import wavfile

    # Read the audio bytes as a WAV file
    wav_io = io.BytesIO(audio_bytes.getvalue())
    sample_rate, audio_data = wavfile.read(wav_io)

    # If stereo, convert to mono by averaging channels
    if len(audio_data.shape) == 2:
        audio_data = np.mean(audio_data, axis=1)

    # Compute STFT
    f, t, Zxx = stft(audio_data, fs=sample_rate, nperseg=1024)

    # Plot spectrogram
    plt.figure(figsize=(10, 6))
    plt.pcolormesh(t, f, 20 * np.log10(np.abs(Zxx)), shading='gouraud')
    plt.colorbar(label='Intensity [dB]')
    plt.title('STFT Spectrogram')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.ylim(0, sample_rate / 2)
    plt.tight_layout()
    st.pyplot(plt)
    st.write("Sample Rate:", sample_rate)

    # Playback the recorded audio
    st.audio(audio_bytes, format='audio/wav')

