<img width="1280" alt="readme-banner" src="https://github.com/user-attachments/assets/35332e92-44cb-425b-9dff-27bcf1023c6c">

# PIKACHU 🎯


## Basic Details
### Team Name: Geeks


### Team Members
- Team Lead: Edwin Joy - SCMS School of Engineering & Technology
- Member 2: Gauri Vinod Nair - SCMS School of Engineering & Technology
- Member 3: Gouri K Mineesh - SCMS School of Engineering & Technology

### Project Description
This project is an Automatic Pikachu-Voice Converter that records your voice, then modifies and replays it with a pitch-perfect Pikachu sound effect! A fun tool to bring out your inner Pokémon.

### The Problem (that doesn't exist)
There are too many boring, human-sounding voices in the world. Where's the charm, the spark, the pika-pika?

### The Solution (that nobody asked for)
With Pikachu-ify, you can instantly transform your voice into Pikachu's! Just press a button, say anything, and let our program handle the rest. Say goodbye to mundane, and hello to electric vocal transformations!

## Technical Details
### Technologies/Components Used
For Software:
- Languages - Python,HTML
- Frameworks - Flask (for the backend server)
- Libraries used -  PyAudio (for recording), NumPy (for audio processing), Soundfile (for saving modified audio), HTTPServer (for web-based interaction)
- Tools used - Visual Studio Code, Web browser for testing

For Hardware:

Main Components:

Microphone (to capture your voice)
Computer or Raspberry Pi (to run the software and process audio)
Speakers or Headphones (to play back the modified audio)

Specifications:
Microphone: Standard USB or 3.5mm microphone
Computer Specifications: Minimum 4GB RAM, 2 GHz Processor (to handle real-time audio processing)
Storage: 10 MB (to store temporary audio files)
Audio Output: Speakers or Headphones for playback with clear audio output

Tools Required:
USB cables (for connecting microphone and other peripherals)
Soldering kit (optional, if connecting the microphone to a custom hardware setup)
Debugging tools (such as a multimeter, if testing audio circuitry with custom setups)
Hardware enclosures (to protect equipment if using Raspberry Pi or portable setup)

### Implementation
For Software: 
1. Setting Up the Server
Begin by setting up a basic HTTP server to handle client requests to start audio recording and playback. Use Python’s http.server for a simple web interface.
2. Recording Audio
Record audio using pyaudio. Capture microphone input at a sample rate of 44100 Hz with a duration defined by the user.
3. Applying Pitch Modification
Use numpy to modify the pitch by changing the sample rate.
4. Web Interface for User Interaction
Create a basic HTML front end with a button to start recording and playback.
5. Running the Server
Use Python’s HTTPServer to run the server and handle incoming requests.
6. Testing
Access http://localhost:8000 in a browser to test recording, pitch modification, and playback.

# Installation
[commands]
1. pip install numpy
2. pip install pyaudio
3. pip install soundfile

# Run

BACK-END

import pyaudio
import numpy as np
import soundfile as sf
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

# Function to record audio
def record_audio(filename, duration=5):
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

# Function to modify the pitch of the audio
def modify_pitch(filename, pitch_factor=1.5):
    data, samplerate = sf.read(filename)
    new_data = np.interp(np.arange(0, len(data), pitch_factor), np.arange(0, len(data)), data)
    sf.write('modified_' + filename, new_data, samplerate)

# Define a class for handling HTTP requests
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            # Serve the HTML page with the Start button
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open('index.html', 'rb') as f:
                self.wfile.write(f.read())

        elif self.path.startswith("/start_recording"):
            # Parse query parameters if any (for duration, etc.)
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            duration = int(params.get('duration', [5])[0])  # Default to 5 seconds

            # Record and modify audio
            record_audio('original.wav', duration)
            modify_pitch('original.wav')

            # Send the modified audio as the response
            self.send_response(200)
            self.send_header('Content-type', 'audio/wav')
            self.end_headers()
            with open('modified_original.wav', 'rb') as f:
                self.wfile.write(f.read())

# Set up the server
if __name__ == "__main__":
    server_address = ('', 8000)  # Listen on all interfaces
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print("Server running on http://localhost:8000")
    httpd.serve_forever()


FRONT-END

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pikachu Recorder</title>
    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            height: 100vh;
            background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            background-color: rgba(62, 57, 210, 0.567);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        h1 {
            color: #ffffff;
            margin: 0;
        }
        /* Start Button Style */
        .button-wrapper {
            display: inline-block;
            position: relative;
            top: 15px;
        }
        .button-wrapper a {
            display: block;
            width: 200px;
            height: 40px;
            line-height: 40px;
            font-size: 18px;
            font-family: sans-serif;
            text-decoration: none;
            color: #000000;
            background-color: #4CAF50;
            text-align: center;
            position: relative;
            transition: all 0.35s;
            border-radius: 5px;
            overflow: hidden;
        }
        .button-wrapper a span {
            position: relative;
            z-index: 2;
        }
        .button-wrapper a::after {
            position: absolute;
            content: "";
            top: 0;
            left: 0;
            width: 0;
            height: 100%;
            background: #ff003b;
            transition: all 0.35s;
            border-radius: 5px;
        }
        .button-wrapper a:hover {
            color: #fff;
        }
        .button-wrapper a:hover::after {
            width: 100%;
        }

        /* Gradient animation keyframes */
        @keyframes gradient {
            0% {
                background-position: 0% 50%;
            }
            50% {
                background-position: 100% 50%;
            }
            100% {
                background-position: 0% 50%;
            }
        }
    </style>
    <script>
        function startRecording() {
            fetch('/start_recording')
                .then(response => response.blob())
                .then(blob => {
                    const audioUrl = URL.createObjectURL(blob);
                    const audio = new Audio(audioUrl);
                    audio.play();
                });
        }
    </script>
</head>
<body>
    <div class="container">
        <h1>! Pikachu !</h1>
        <div class="button-wrapper">
            <a href="#" onclick="startRecording()"><span>Record</span></a>
        </div>
    </div>
</body>
</html>

### Project Documentation
For Software:
Our project, **PIKACHU**, is a simple yet entertaining web application that allows users to record audio directly from their browser and instantly replay it with a humorous pitch modification. This Python-based web server captures a 5-second audio recording, adjusts its pitch, and plays it back with a fun twist, making it ideal for quick and playful voice transformations.

### The Problem (that doesn't exist)
Have you ever wished your voice could sound like a cartoon character at the click of a button? Or maybe you've wondered what you'd sound like as a supervillain? This project solves the non-existent, yet irresistible problem of *instant voice transformation.*

### The Solution (that nobody asked for)
With the press of a button, this web application captures audio, transforms it with a funny pitch effect, and replays it instantly. The solution you didn’t know you needed for surprising friends or just giving yourself a laugh!



# Screenshots

![Screenshot1]![front end](https://github.com/user-attachments/assets/f40f23a7-be2b-41ac-b462-fc42bdf98e9f)

![Screenshot2]![back end](https://github.com/user-attachments/assets/5eb696b4-f264-48dd-aaea-f0aec3ba87e3)


![Screenshot3]![webpage](https://github.com/user-attachments/assets/5b3a4f7a-e2a7-40b7-ad9c-984669e859bf)

# Diagrams
Serve HTML Page
       |
       v
User Clicks "Start"
       |
       v
Trigger /start_recording Endpoint
       |
       v
Record Audio (5 seconds)
       |
       v
Modify Pitch of Audio
       |
       v
Return Modified Audio
       |
       v
Playback Audio in Browser


For Hardware:

# Schematic & Circuit
   Microphone
       |
       |----> Audio Interface (if necessary)
       |
    [Computer]
       |
       |----> USB
       |
    [Microcontroller] (Raspberry Pi/Arduino)


# Build Photos
Screenshots added above.

### Project Demo
# Video
[Add your demo video link here]
*Explain what the video demonstrates*

# Additional Demos
[Add any extra demo materials/links]

## Team Contributions
- [Name 1]: [Specific contributions]
- [Name 2]: [Specific contributions]
- [Name 3]: [Specific contributions]

---
Made with ❤️ at TinkerHub Useless Projects 

![Static Badge](https://img.shields.io/badge/TinkerHub-24?color=%23000000&link=https%3A%2F%2Fwww.tinkerhub.org%2F)
![Static Badge](https://img.shields.io/badge/UselessProject--24-24?link=https%3A%2F%2Fwww.tinkerhub.org%2Fevents%2FQ2Q1TQKX6Q%2FUseless%2520Projects)



