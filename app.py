from flask import Flask, render_template, request, redirect, url_for
import json
import random
import pygame

app = Flask(__name__)

# 加载音乐库
with open("music.json", 'r') as f:
    music_library = json.load(f)

# 初始化播放器
player = pygame.mixer
player.init()

# BPM → 情绪映射
def map_bpm_to_emotion(bpm):
    if bpm < 65:
        return "Sad"
    elif bpm > 100:
        return "Happy"
    else:
        return "Calm"

# 情绪文案
emotion_messages = {
    "Happy": (
        "A lively heartbeat detected!\n"
        "You seem to be glowing with joy and vitality.\n"
        "Let’s celebrate your energy with uplifting music."
    ),
    "Sad": (
        "Your heart rhythm suggests a quiet, low emotional state.\n"
        "You're not alone — even cloudy skies pass.\n"
        "Let these gentle tunes carry you through."
    ),
    "Calm": (
        "Your heart beats with steady rhythm and clarity.\n"
        "You seem to be in a peaceful, centered state.\n"
        "Let the music flow gently with your breath."
    )
}


# 封面图路径
emotion_covers = {
    "Happy": "images/Mask group-1.png",
    "Sad": "images/Mask group-2.png",
    "Calm": "images/Mask group.png"
}

@app.route("/")
def index():
    # 初始页面（无音乐）
    return render_template("index.html", track_title=None)

@app.route("/simulate", methods=["POST"])
def simulate():
    try:
        bpm = int(request.form['bpm'])
    except:
        bpm = 76

    emotion = map_bpm_to_emotion(bpm)
    matches = [track for track in music_library if track['emotion'].lower() == emotion.lower()]
    track = random.choice(matches) if matches else {"title": "", "filepath": "", "artist": ""}

    try:
        player.music.load(track['filepath'])
        player.music.play()
    except:
        pass  # 忽略加载错误

    return render_template("index.html",
                           bpm=bpm,
                           emotion=emotion,
                           emotion_text=emotion_messages[emotion],
                           track_title=track['title'],
                           track_artist=track['artist'],
                           cover_image=emotion_covers[emotion],
                           track_path=track['filepath'])

@app.route("/stop", methods=["POST"])
def stop():
    player.music.stop()
    # 保留界面但不再播放音乐
    return render_template("index.html",
                           bpm=None,
                           emotion="Calm",
                           emotion_text="Music stopped. You can try again.",
                           track_title=None,
                           track_artist=None,
                           cover_image=emotion_covers["Calm"],
                           track_path=None)

if __name__ == '__main__':
    app.run(debug=True)
