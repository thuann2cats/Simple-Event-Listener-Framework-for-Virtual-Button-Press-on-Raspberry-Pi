from gtts import gTTS
import os
import time
import traceback
from threading import Event
import pygame

# have to install:
# pip install gTTS (https://www.codingem.com/python-text-to-speech/)
# pip install pygame
# and then, if there's an error, may have to install this (on Linux):
# sudo apt-get install libsdl2-mixer-dev


class Speaker:
    '''This class contains a static method that will say a sentence to an audio output. It uses two other Python libraries from the Internet:
    + The gtts library (Google Text-To-Speech library) can generate an mp3 audio file from text.
    + The pygame library provides methods to play, pause or stop that mp3 audio file.
    
    The audio file generated by the Google Text-To-Speech library is temporary and will be deleted at the end of the speak() method.
    
    '''
    
    
    @staticmethod
    def speak(cancelFlag=Event(), text=""):
        '''This method will create an audio version of the strings contained in the 'text' variable, then play this audio file.
        
        text: the text to be read out
        cancelFlag (optional): a threading.Event object that functions as a way for the programmer to stop the audio reading (for example, user presses a CANCEL key or hovers a CANCEL sensor). If omitted, then the text will just be read from beginning to end
        '''
        
        tts = gTTS(text=text, lang="en", slow=False)
        # create a unique file name according to current time
        currentTime = time.strftime("%Y%m%d%f-%H%M%S")
        fileName = f"{currentTime}_tempAudio.mp3"
        tts.save(fileName)
        
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(fileName)
        pygame.mixer.music.play()
        
        
        while pygame.mixer.music.get_busy()==True:
            
            # periodically check every 0.25 seconds, if the cancelFlag event has been set to true, then stop the audio and exit
            
            time.sleep(0.25)
            if cancelFlag.is_set():
                pygame.mixer.music.stop()
                Speaker.speak(Event(), "Cancelled")
                break
            else:
                pass
        
        
        # delete the temporary mp3 file
        try:
            os.remove(fileName)
        except OSError as e:
            traceback.print_exc()
            print(e)

    @staticmethod
    def playFile(cancelFlag=Event(), fileName="memo.wav"):
        '''This method is similar to the method above, except that the sound file already exists, and is not the result of converting text to speech.
        
        cancelFlag (optional): a threading.Event object that functions as a way for the programmer to stop the audio reading (for example, user presses a CANCEL key or hovers a CANCEL sensor). If omitted, then the text will just be read from beginning to end
        '''
        
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(fileName)
        pygame.mixer.music.play()
        
        
        while pygame.mixer.music.get_busy()==True:
            
            # periodically check every 0.25 seconds, if the cancelFlag event has been set to true, then stop the audio and exit
            
            time.sleep(0.25)
            if cancelFlag.is_set():
                pygame.mixer.music.stop()
                break
            else:
                pass
        
        
        # delete the temporary mp3 file
        try:
            # os.remove(fileName)
            pass
        except OSError as e:
            traceback.print_exc()
            print(e)
        
# Sample usage:
# Speaker.speak("This is pygame testing")