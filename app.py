"""
Desk Buddy V1 - AI WebSocket Server
-----------------------------------
This server acts as the brain for the Desk Buddy robot. It listens for a WebSocket connection
from an ESP32, receives raw audio data (from an INMP441 microphone), processes it through
the Gemini 1.5 Flash API for a response, and converts that response back into an MP3 audio 
file using Google Text-to-Speech (gTTS) to send back to the ESP32.

Prerequisites:
- Python 3.8+
- pip install fastapi uvicorn websockets google-generativeai gtts python-dotenv

Setup:
- Create a `.env` file in the same directory as this script.
- Add your Gemini API key: GEMINI_API_KEY=your_api_key_here
- Run the server: uvicorn app:app --host 0.0.0.0 --port 8000
"""

import os
import wave
from fastapi import FastAPI, WebSocket
import google.generativeai as genai
from gtts import gTTS
from dotenv import load_dotenv

# ==================*========================
# 1. SETUP & CONFIGURATION
# ===================*=======================
# Load environment variables from the .env file
load_dotenv()

# Configure the Gemini API client
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Please check your .env file.")
genai.configure(api_key=api_key)

# Initialize the Gemini model. 
# We use 'gemini-1.5-flash' because it natively supports audio inputs and is incredibly fast.
model = genai.GenerativeModel('gemini-1.5-flash')

# Initialize the FastAPI application
app = FastAPI()

# ======================*====================
# 2. WEBSOCKET ENDPOINT
# =======================*===================
@app.websocket("/ws")
async def desk_buddy_endpoint(websocket: WebSocket):
    """
    Handles the continuous WebSocket connection with the ESP32.
    """
    await websocket.accept()
    print("🤖 Desk Buddy is connected and listening!")
    
    try:
        while True:
            # --- STEP 1: RECEIVE AUDIO ---
            print("Waiting for audio stream from ESP32...")
            # For this MVP, we wait for the ESP32 to send the entire recorded chunk as binary bytes
            audio_bytes = await websocket.receive_bytes()
            print("Audio received! Processing data...")

            # Save the raw PCM data sent by the INMP441 microphone.
            # INMP441 specs: 16-bit, 16000Hz, Mono
            raw_filename = "input.raw"
            with open(raw_filename, "wb") as f:
                f.write(audio_bytes)
                
            # Convert the raw PCM data into a standard WAV file so Gemini can process it.
            wav_filename = "input.wav"
            with wave.open(wav_filename, 'wb') as wav_file:
                wav_file.setnchannels(1)     # 1 Channel (Mono)
                wav_file.setsampwidth(2)     # 2 bytes = 16-bit resolution
                wav_file.setframerate(16000) # 16kHz Sample Rate
                with open(raw_filename, "rb") as raw_file:
                    wav_file.writeframes(raw_file.read())

            # --- STEP 2: PROCESS WITH AI (GEMINI) ---
            print("Uploading audio to Gemini...")
            audio_file = genai.upload_file(path=wav_filename)
            
            # This is Desk Buddy's core system prompt. Change this to alter his personality 😏.
            prompt = (
                "You are Desk Buddy, a helpful and slightly sarcastic desktop robot. "
                "Keep your answer to 1 or 2 short sentences. Answer the user."
            )
            
            print("Generating response...")
            response = model.generate_content([prompt, audio_file])
            print(f"Desk Buddy says: {response.text}")

            # --- STEP 3: TEXT-TO-SPEECH (TTS) ---
            print("Converting text to speech...")
            # Convert Gemini's text response into spoken audio using Google TTS
            tts = gTTS(text=response.text, lang='en', slow=False)
            output_filename = "output.mp3"
            tts.save(output_filename)

            # --- STEP 4: SEND RESPONSE TO ESP32 ---
            print("Sending audio response back to ESP32...")
            # Read the generated MP3 file and send it over the WebSocket as binary data
            with open(output_filename, "rb") as f:
                audio_out = f.read()
            
            await websocket.send_bytes(audio_out)
            print("Response delivered! Waiting for the next command...\n")

    except Exception as e:
        print(f"⚠️ Connection closed or interrupted: {e}")

# Whom to Thganks
# ---> Yeah its me your BRO[Unless you are a girl] `ARNAB` ;