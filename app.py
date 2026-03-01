import speech_recognition as sr
import google.generativeai as genai
import os

# ==========================================
# 1. SETUP THE AI BRAIN (GEMINI)
# ==========================================
# Replace with your actual API key from Google AI Studio
API_KEY = "AIzaSyBn1bIaI9R8wvxMZH49Bsod34OY6VGeMwk" 
genai.configure(api_key=API_KEY)

# Use the flash model for fast, real-time responses
model = genai.GenerativeModel('gemini-2.5-flash')

# ==========================================
# 2. SETUP THE EARS (MAC MICROPHONE)
# ==========================================
recognizer = sr.Recognizer()

# ==========================================
# 3. THE VOICE ENGINE (MAC -> BLUETOOTH -> ROBOT)
# ==========================================
def speak(text):
    """Cleans the text and speaks it out loud through the Mac's output."""
    # Clean up punctuation that might break the Mac's 'say' terminal command
    clean_text = text.replace("'", "").replace('"', "").replace('*', '').replace('\n', ' ')
    
    print(f"\n🤖 ROBOT SAYS: {clean_text}\n")
    
    # The 'say' command is built into macOS. 
    # Since your Mac is connected to the ESP32 Bluetooth, this plays on the robot!
    os.system(f"say '{clean_text}'")

# ==========================================
# 4. THE MAIN BRAIN LOOP
# ==========================================
def listen_and_think():
    with sr.Microphone() as source:
        print("Calibrating for room noise... (shhh)")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        
        print("🟢 LISTENING... Speak directly into your Mac now!")
        try:
            # Listen to the microphone
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("Processing your voice...")
            
            # Convert speech to text using Google's free speech recognition
            user_text = recognizer.recognize_google(audio)
            print(f"🗣️  YOU SAID: {user_text}")
            
            # Give the AI a personality and limit its response length
            print("🧠 Thinking...")
            system_prompt = " (You are a helpful, witty robot companion sitting on a desk  and you are created by ARNAB. Keep your answer conversational, fun, and strictly under 2 sentences.)"
            prompt = user_text + system_prompt
            
            # Send to Gemini
            response = model.generate_content(prompt)
            
            # Speak the answer
            speak(response.text)
            
        except sr.UnknownValueError:
            print("⚠️  Sorry, I couldn't understand the audio.")
        except sr.RequestError:
            print("⚠️  Network error with the speech recognition service.")
        except Exception as e:
            print(f"⚠️  Error: {e}")

# ==========================================
# RUN THE PROGRAM
# ==========================================
if __name__ == "__main__":
    os.system("clear")
    print("========================================")
    print("      ROBOT BRAIN ONLINE (APP.PY)       ")
    print("========================================")
    
    speak("System online. My hardware is linked, and my brain is ready.")
    
    while True:
        # We use push-to-talk so it doesn't accidentally listen to its own voice playing from the speaker!
        input("\n👉 Press ENTER to start listening (or Ctrl+C to quit)...")
        listen_and_think()