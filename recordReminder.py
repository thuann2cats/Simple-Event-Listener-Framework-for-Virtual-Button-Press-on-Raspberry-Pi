import pyaudio      #pip install pyaudio
import wave         #pip install wave
# import keyboard     #pip install keyboard
import os
from speaker import Speaker
from threading import Event

PYAUDIO = pyaudio.PyAudio()

class Reminder:
    def __init__(self, fileName, cancelFlag):
       self.memo = fileName              #only one audio file can exist at a time with this program
       self.FORMAT = pyaudio.paInt16
       self.CHANNELS = 1
       self.FPB = 4096
       self.RATE = 44100
    #    self.audio = pyaudio.PyAudio()
       self.audio = pyaudio.PyAudio()
       self.istream = self.audio.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.FPB, input_device_index=1) 
       self.cancelFlag = cancelFlag

    def record(self):
        self.frames = []
        seconds = 45
        #recording start
        print("recording begins...")
        
        
        for i in range(0, int(self.RATE / self.FPB * seconds)):
            # print("inside for loop!")
            data = self.istream.read(self.FPB)
            self.frames.append(data)

            # if keyboard.is_pressed('q'):                        #replace with hover interrupt to stop recording before the 30 seconds is up
            #     break
            if self.cancelFlag.is_set():
                break

        #recording end
        self.istream.stop_stream()
        self.istream.close()
        self.audio.terminate()
        Speaker.speak(Event(), "Recording completed.")
        print("done recording")
        print()
        #compile frames into .wave file
        self.wf = wave.open(self.memo, 'wb')
        self.wf.setnchannels(self.CHANNELS)
        self.wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
        self.wf.setframerate(self.RATE)
        self.wf.writeframes(b''.join(self.frames))
        self.wf.close()

    def speak(self):
            #set filename of memo to read
            wave_file = wave.open(self.memo, "rb")
            oaudio = pyaudio.PyAudio()
            ostream = oaudio.open(format=self.audio.get_format_from_width(wave_file.getsampwidth()), 
                                          channels=wave_file.getnchannels(), rate=wave_file.getframerate(), output=True)
            data = wave_file.readframes(1024)
            while data:
                ostream.write(data)
                data = wave_file.readframes(1024)

                # if keyboard.is_pressed('q'):        #replace with hover interrupt, stops audio and deletes file
                #     ostream.stop_stream()
                #     ostream.close()
                #     wave_file.close()
                #     oaudio.terminate()
                #     os.remove(self.memo)
                #     break
            ostream.stop_stream()
            ostream.close()
            wave_file.close()
            oaudio.terminate()

# import pyaudio      #pip install pyaudio
# import wave         #pip install wave
# import keyboard     #pip install keyboard
# import os
# from speaker import Speaker
# from threading import Event

# class Reminder:
#     def __init__(self, cancelFlag=Event()):
#        self.memo = "memo.wav"              #only one audio file can exist at a time with this program
#        self.FORMAT = pyaudio.paInt16
#        self.CHANNELS = 1
#        self.FPB = 1024
#        self.RATE = 44100
#        self.audio = pyaudio.PyAudio()
#        self.istream = self.audio.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.FPB) 
       
#        self.cancelFlag = cancelFlag # this instance variable will be checked during the process of recording, to see when user wants to stop

#     def record(self):
#         frames = []
#         seconds = 10
#         #recording start
#         # Speaker.speak(Event(), "Please start recording...")
#         print("Begin recording")
        
#         for i in range(0, int(self.RATE / self.FPB * seconds)):
#             print("inside for loop")
#             data = self.istream.read(self.FPB)
#             frames.append(data)

#             if self.cancelFlag.is_set():
#                 break

#         #recording end
#         self.istream.stop_stream()
#         self.istream.close()
#         self.audio.terminate()
#         # Speaker.speak(Event(), "Recording completed!")
#         print("Recording completed")
#         #compile frames into .wave file
#         wf = wave.open(self.memo, 'wb')
#         wf.setnchannels(self.CHANNELS)
#         wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
#         wf.setframerate(self.RATE)
#         wf.writeframes(b''.join(frames))
#         wf.close()
        
#         print("done here here")

#     def speak(self):
#         print("speaking")
#         #set filename of memo to read
#         wave_file = wave.open(self.memo, "rb")
#         oaudio = pyaudio.PyAudio()
#         ostream = oaudio.open(format=self.audio.get_format_from_width(wave_file.getsampwidth()), 
#                                         channels=wave_file.getnchannels(), rate=wave_file.getframerate(), output=True)
#         data = wave_file.readframes(1024)
#         while data:
#             ostream.write(data)
#             data = wave_file.readframes(1024)

#             # if keyboard.is_pressed('q'):        #replace with hover interrupt, stops audio and deletes file
#             #     ostream.stop_stream()
#             #     ostream.close()
#             #     wave_file.close()
#             #     oaudio.terminate()
#             #     os.remove(self.memo)
#             #     break
#         ostream.stop_stream()
#         ostream.close()
#         wave_file.close()
#         oaudio.terminate()
#         print("DONE speaking")
        
# rm = Reminder()
# input("Press Enter to continue and record something...")
# rm.record()
# input("Press Enter to continue...")
# rm.speak()