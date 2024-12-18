# audio_processor.py
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import os

# Directory for saving plots
IMAGE_CACHE_DIR = 'images'

# Ensure the directory for cached images exists
if not os.path.exists(IMAGE_CACHE_DIR):
    os.makedirs(IMAGE_CACHE_DIR)

def generate_and_cache_plot(filename, plot_type):
    samples, sample_rate = librosa.load(filename)

    # Check if the plot already exists in cache
    image_path = os.path.join(IMAGE_CACHE_DIR, f"{plot_type}.png")

    if os.path.exists(image_path):  # Check if the plot is cached
        return f"/images/{plot_type}.png"  # Return static URL path

    fig = plt.figure(figsize=(14, 8))  # Larger figure size
    try:
        if plot_type == 'raw_wave':
            ax = fig.add_subplot(211)
            ax.set_title('Raw Wave')
            ax.set_ylabel('Amplitude')
            librosa.display.waveshow(samples, sr=sample_rate)

        elif plot_type == 'amplitude_spectrum':
            ax = fig.add_subplot(212)
            ax.set_title('Amplitude Spectrum')
            ax.set_ylabel('Amplitude (dB)')
            D = librosa.stft(samples)
            D_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
            librosa.display.specshow(D_db, sr=sample_rate, x_axis='time', y_axis='log')

        elif plot_type == 'spectrogram':
            ax = fig.add_subplot(211)
            ax.set_title('Spectrogram')
            ax.set_ylabel('Frequency (Hz)')
            S = librosa.feature.melspectrogram(y=samples, sr=sample_rate)
            librosa.display.specshow(librosa.power_to_db(S, ref=np.max), y_axis='mel', x_axis='time')

        elif plot_type == 'chromagram':
            ax = fig.add_subplot(212)
            ax.set_title('Chromagram')
            ax.set_ylabel('Chromagram')
            chroma = librosa.feature.chroma_stft(y=samples, sr=sample_rate)
            librosa.display.specshow(chroma, y_axis='chroma', x_axis='time')

        # Save the plot to a file
        plt.savefig(image_path, format='png')
        plt.close(fig)

        return f"/static/images/{plot_type}.png"  # Return static URL path
    except Exception as e:
        print(f"Error generating plot for {plot_type}: {e}")
        return None
