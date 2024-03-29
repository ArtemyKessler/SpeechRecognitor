import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime

# настройки
opts = {
    "alias": ('соня', 'сонечка', 'сонька', 'слуга', 'девочка робот', 'саня',
              'сониа'),
    "tbr": ('скажи', 'расскажи', 'покажи', 'сколько', 'произнеси'),
    "cmds": {
        "ctime": ('текущее время', 'сейчас времени', 'который час'),
        "radio": ('включи музыку', 'воспроизведи радио', 'включи радио'),
        "stupid1": ('расскажи анекдот', 'рассмеши меня', 'ты знаешь анекдоты')
    }
}

# функции


def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()


def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language="ru-RU").lower()
        print("[log] Распознано: " + voice)

        if voice.startswith(opts["alias"]):
            # обращаются к Кеше
            cmd = voice

            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()

            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()

            # распознаем и выполняем команду
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])

    except sr.UnknownValueError:
        print("[log] Голос не распознан!")
    except sr.RequestError as e:
        print("[log] Неизвестная ошибка, проверьте подключение!")


def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c, v in opts['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt

    return RC


def execute_cmd(cmd):
    if cmd == 'ctime':
        # сказать текущее время
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))
        os.execv("C:\\Users\\USER\\Desktop\\Projects\\SpeechRecognitor\\Sonya.py")

    elif cmd == 'radio':
        # воспроизвести радио
        os.system(
            "C:\\Users\\USER\\Desktop\\Projects\\SpeechRecognitor\\stream.m3u")
        os.execv("C:\\Users\\USER\\Desktop\\Projects\\SpeechRecognitor\\Sonya.py")

    elif cmd == 'stupid1':
        # рассказать анекдот
        speak("Идет медведь по лесу, видит машина горит. Сел в нее и сгорел")
        os.execv("C:\\Users\\USER\\Desktop\\Projects\\SpeechRecognitor\\Sonya.py")

    else:
        print('Команда не распознана, повторите!')
        os.execv("C:\\Users\\USER\\Desktop\\Projects\\SpeechRecognitor\\Sonya.py")


# запуск
r = sr.Recognizer()
m = sr.Microphone(device_index=1)

with m as source:
    r.adjust_for_ambient_noise(source)

speak_engine = pyttsx3.init()

speak("Здравствуйте, повелитель")
speak("Соня готова вам помочь")

stop_listening = r.listen_in_background(m, callback)
while True:
    time.sleep(0.1)  # infinity loop
