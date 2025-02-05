import speech_recognition as sr
import pyttsx3
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import webbrowser
import time

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Set speech speed

# Spotify API credentials (Replace with your own)
SPOTIPY_CLIENT_ID = "1148d273690b4f47afb8e3178d2d73f3"
SPOTIPY_CLIENT_SECRET = "c8042105cd33446a8245093d8c452e80"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID,
                                                           client_secret=SPOTIPY_CLIENT_SECRET))

# Spotify playlist ID for recommendations
SPOTIFY_PLAYLIST_URL = "https://open.spotify.com/embed/playlist/7j0XUJDRGzdiXDe3QIJemc"

# Predefined friendly responses
RESPONSES = {
    "i am tired": "No, you are a strong and amazing person! Keep going!",
    "i feel sad": "Hey, I'm here for you! You're not alone. Keep smiling!",
    "who are you": "I am Hermit, your friendly assistant and companion!",
    "hello": "Hello there! How can I make your day better?",
    "thank you": "You're welcome! Always here to help!",
}

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen for user voice input."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio).lower()
            return text
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            speak("Could not connect to the internet.")
            return ""

def play_song(song_name):
    """Search for a song on Spotify and play it in a browser."""
    results = sp.search(q=song_name, limit=1, type="track")
    if results['tracks']['items']:
        song_url = results['tracks']['items'][0]['external_urls']['spotify']
        speak(f"Playing {song_name}")
        webbrowser.open(song_url)  # Opens the song in the default browser
    else:
        speak("Sorry, I couldn't find that song.")

def play_playlist():
    """Play a recommended playlist."""
    speak("Playing your recommended playlist.")
    webbrowser.open(SPOTIFY_PLAYLIST_URL)

def hermit_assistant():
    """Main function to handle user interaction."""
    speak("Hello! Say 'hello' to start.")
    
    while True:
        user_input = listen()
        
        if "hello" in user_input:
            speak("Hi! I'm Hermit, your friend. How can I help you?")
        
        elif "play playlist" in user_input:
            play_playlist()
        
        elif "play" in user_input:
            song_name = user_input.replace("play", "").strip()
            if song_name:
                play_song(song_name)
            else:
                speak("Please tell me which song to play.")

        elif user_input in RESPONSES:
            speak(RESPONSES[user_input])
        
        elif "good night" in user_input or "shutdown" in user_input:
            speak("Good night! See you soon.")
            break
        
        elif user_input:
            speak("I am here to play songs and talk with you.")

if __name__ == "__main__":
    hermit_assistant()
