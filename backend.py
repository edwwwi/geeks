import os
import pyaudio
import numpy as np
import soundfile as sf
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

# Function to record audio
def record_audio(filename, duration=5):
    try:
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
        print(f"Recording for {duration} seconds...")
        frames = []

        for _ in range(int(44100 / 1024 * duration)):
            data = stream.read(1024)
            frames.append(np.frombuffer(data, dtype=np.int16))  # Convert bytes to numpy array

        print("Finished recording.")
        stream.stop_stream()
        stream.close()
        audio.terminate()

        # Concatenate all frames to create a single numpy array
        audio_data = np.concatenate(frames)

        # Save the audio to a file
        sf.write(filename, audio_data, 44100)  # Save as WAV file with sample rate
    except Exception as e:
        print(f"Error during recording: {e}")

# Function to modify the pitch of audio
def modify_pitch(filename, pitch_factor=1.5):
    try:
        data, samplerate = sf.read(filename)
        new_data = np.interp(np.arange(0, len(data), pitch_factor), np.arange(0, len(data)), data)
        sf.write('modified_' + filename, new_data, samplerate)
    except Exception as e:
        print(f"Error modifying pitch: {e}")

# Define a class for handling HTTP requests
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            # Serve the HTML page with the Start button
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            try:
                with open(os.path.join('templates', 'index.html'), 'rb') as f:
                    self.wfile.write(f.read())
            except FileNotFoundError:
                self.wfile.write(b"<h1>index.html not found in templates/</h1>")
                print("Error: index.html not found.")

        elif self.path.startswith("/start_recording"):
            # Parse query parameters (for recording duration, etc.)
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            duration = int(params.get('duration', [5])[0])  # Default duration is 5 seconds

            # Record and modify audio
            record_audio('original.wav', duration)
            modify_pitch('original.wav')

            # Send the modified audio as the response
            try:
                self.send_response(200)
                self.send_header('Content-type', 'audio/wav')
                self.end_headers()
                with open('modified_original.wav', 'rb') as f:
                    self.wfile.write(f.read())
            except FileNotFoundError:
                self.wfile.write(b"<h1>Audio file not found.</h1>")
                print("Error: Audio file not found.")

# Set up and run the HTTP server
if __name__ == "__main__":
    try:
        server_address = ('', 8000)  # Listen on all interfaces on port 8000
        httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
        print("Server running at http://localhost:8000")
        httpd.serve_forever()
    except Exception as e:
        print(f"Server error: {e}")
