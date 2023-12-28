#!/usr/bin/env python
# coding: utf-8

# In[7]:


import ipywidgets as widgets
from IPython.display import display
from threading import Thread
from queue import Queue
import pyttsx3
import speech_recognition as sr
from translate import Translator

messages = Queue()
recordings = Queue()

record_button = widgets.Button(
    description='Record',
    disabled=False,
    button_style="success",
    icon='microphone'
)

stop_button = widgets.Button(
    description='Stop',
    disabled=False,
    button_style="warning",
    icon='stop'
)

output = widgets.Output()

engine = pyttsx3.init()

def record_microphone(recognizer):
    while recordings.qsize() > 0:
        try:
            with sr.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                # Recognize speech using Google's API
                text = recognizer.recognize_google(audio)
                text = text.lower()
                print(f'Recognized: {text}')

                # Translate the recognized text to Greek using the translate library
                if text:  # Check if text is not None
                    translator = Translator(from_lang="en", to_lang="el")
                    translation = translator.translate(text)
                    print(f'Translation to Greek: {translation}')

                    # Text-to-speech for the translated text
                    #engine.say(translation)
                    #engine.runAndWait()

        except sr.UnknownValueError:
            recognizer = sr.Recognizer()
            continue

def start_recording(data):
    messages.put(True)
    
    with output:
        display('Starting...')
        recognizer = sr.Recognizer()  # Create a new recognizer instance for each recording
        record = Thread(target=record_microphone, args=(recognizer,))
        recordings.put(record)  # Add the record thread to the recordings queue
        record.start()

def stop_recording(data):
    with output:
        messages.get()
        display('Stopped.')

        # Stop all recording threads
        while not recordings.empty():
            record = recordings.get()
            record.join()  # Wait for the thread to finish

record_button.on_click(start_recording) 
stop_button.on_click(stop_recording)

display(record_button, stop_button, output)


# In[ ]:




