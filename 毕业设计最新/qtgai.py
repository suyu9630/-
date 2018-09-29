from gtts import gTTS
import os
tts = gTTS(text='血逼', lang='zh-yue')
tts.save("hello.mp3")
os.system('play hello.mp3')
