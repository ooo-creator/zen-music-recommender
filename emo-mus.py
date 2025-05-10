import json
import pygame
import threading
import time
import random
from datetime import datetime

stop_flag = False

def wait_for_enter():
    global stop_flag
    input("▶️ Press Enter anytime to stop playback...\n")
    stop_flag = True
    pygame.mixer.music.stop()

def play_single_track(filepath):
    global stop_flag
    stop_flag = False

    pygame.mixer.init()
    pygame.mixer.music.load(filepath)
    pygame.mixer.music.play()

    listener = threading.Thread(target=wait_for_enter)
    listener.daemon = True
    listener.start()

    print(f"🎵 Now playing: {filepath.split('/')[-1]}")
    while pygame.mixer.music.get_busy() and not stop_flag:
        time.sleep(0.5)

    print("\n👋 Playback stopped. Take care!")

def log_track(track, emotion, matched: bool):
    with open("log.txt", "a") as log:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(
            f"[{now}] Played: {track['title']} | Emotion: {emotion} | Attribute match: {'Yes' if matched else 'No'}\n"
        )

def play_from_emotion(emotion, json_path):
    with open(json_path, 'r') as f:
        library = json.load(f)

    emotion = emotion.lower()
    matches = [track for track in library if track['emotion'].lower() == emotion]
    if not matches:
        print("No matching music found.")
        return

    def match_attributes(track):
        valence = track.get("valence", 0)
        energy = track.get("energy", 0)
        tempo = track.get("tempo", 0)

        if emotion == "happy":
            return valence > 0.7 and energy > 0.7 and tempo > 110
        elif emotion == "sad":
            return valence < 0.3 and energy < 0.5 and tempo < 90
        elif emotion == "calm":
            return 0.5 <= valence <= 0.8 and energy < 0.4 and 60 <= tempo <= 100
        else:
            return True

    filtered = [track for track in matches if match_attributes(track)]

    if filtered:
        track = random.choice(filtered)
        print(f"✅ Selected track fully matches both emotion and musical attributes.")
        full_match = True
    else:
        track = random.choice(matches)
        print(f"⚠️ No track fully matched emotion & attributes. Selected based on emotion only.")
        full_match = False

    log_track(track, emotion, full_match)
    print_intro(emotion)
    play_single_track(track['filepath'])

def print_intro(emotion):
    prompts = {
        "calm": (
            "🫶 Your heart rate appears steady. You seem to be in a calm emotional state.\n"
            "Take this moment to slow down and enjoy a peaceful melody that mirrors your inner stillness.\n"
        ),
        "sad": (
            "😔 Your heart rhythm suggests a low emotional state—perhaps you're feeling stressed or down.\n"
            "You're not alone. Let these gentle tunes accompany you through the cloudy moments.\n"
        ),
        "happy": (
            "😊 A lively heartbeat detected! You seem to be in high spirits.\n"
            "Let’s celebrate your energy with some upbeat, joyful music.\n"
        )
    }
    print(prompts.get(emotion.lower(), "🎶 Playing music for your current emotional state...\n"))

# ✅ Example call – change emotion here:
play_from_emotion("Sad", "music.json")
