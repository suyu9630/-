import speech_recognition
import os
from gtts import gTTS
from pydub import AudioSegment
#sound = AudioSegment.from_mp3("/home/pi/Desktop/sssjj/debug1.mp3")
#sound.export('/home/pi/Desktop/sssjj/123.wav',format="wav")
#print('hello')
r=speech_recognition.Recognizer()
with speech_recognition.AudioFile('/home/pi/Desktop/sssjj/123.wav') as source:
    audio=r.record(source)
    r=r.recognize_google(audio,language='zh-tw')
    print(r)
