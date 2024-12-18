import matplotlib
matplotlib.use('Agg')  # Use the Agg backend for rendering without a GUI
from flask import Flask, render_template, Response
import librosa
import librosa.display
import matplotlib.pyplot as plt
import io
import numpy as np
import os

app = Flask(__name__)

# Define the WAV file path
filename = "C:\\EL-24\\03-01-01-01-01-01-01.wav"  # Update with the correct path

# Ensure the file exists
if not os.path.exists(filename):
    raise FileNotFoundError(f"The file {filename} does not exist!")

@app.route('/')
def index():
    """Main page rendering all plots."""
    return render_template('index.html')

def generate_plot(samples, sample_rate, plot_type):
    """Generate a plot and return it as an in-memory PNG image."""
    fig = plt.figure(figsize=(8, 6))

    try:
        if plot_type == 'raw_wave':
            plt.title('Raw Wave')
            plt.ylabel('Amplitude')
            librosa.display.waveshow(samples, sr=sample_rate)

        elif plot_type == 'amplitude_spectrum':
            plt.title('Amplitude Spectrum')
            plt.ylabel('Amplitude (dB)')
            D = librosa.stft(samples)
            D_db = librosa.amplitude_to_db(abs(D), ref=np.max)
            librosa.display.specshow(D_db, sr=sample_rate, x_axis='time', y_axis='log')

        elif plot_type == 'spectrogram':
            plt.title('Spectrogram')
            plt.ylabel('Frequency (Hz)')
            S = librosa.feature.melspectrogram(y=samples, sr=sample_rate)
            librosa.display.specshow(librosa.power_to_db(S, ref=np.max), y_axis='mel', x_axis='time')

        elif plot_type == 'chromagram':
            plt.title('Chromagram')
            plt.ylabel('Chroma')
            chroma = librosa.feature.chroma_stft(y=samples, sr=sample_rate)
            librosa.display.specshow(chroma, y_axis='chroma', x_axis='time')

        # Save the plot to an in-memory file
        img = io.BytesIO()
        plt.savefig(img, format='png')
        plt.close(fig)
        img.seek(0)
        return img

    except Exception as e:
        print(f"Error generating plot {plot_type}: {e}")
        plt.close(fig)
        return None

@app.route('/plot/<plot_type>')
def plot(plot_type):
    """Route to generate and stream plots dynamically."""
    try:
        samples, sample_rate = librosa.load(filename)
        img = generate_plot(samples, sample_rate, plot_type)
        if img:
            return Response(img, mimetype='image/png')
        else:
            return "Error generating plot", 500
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)
