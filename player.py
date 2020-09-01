# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 11:47:50 2020

@author: Muhammad Abid
"""

import os 
import cv2
import time
import wave
import pyaudio
import argparse
import multiprocessing
import numpy as np
from pynput.keyboard import Listener

"""
This function takes input of commands and filename and start playing audio file
"""
def playAudio(commands, filename):

    # bytes to reaad from the audio file
    chunk_size = 1024
    # Opening audio file
    wf = wave.open(filename, 'rb')
    # create pyaudio class
    p = pyaudio.PyAudio()
    
    #initializing pyaudio class
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(), rate=wf.getframerate(), output=True)

    #reading chunk of data from the audio file
    data = wf.readframes(chunk_size)
    
    # Used to save the state of audio in process
    startPlay = True
    stopPlay = False

    # read until the video or audio is finished
    while data != "" and commands[1] == 0:
        #change local states based when commands updates
        if commands[0] == 1 and stopPlay:
            startPlay = True
            stopPlay = False
        elif commands[0] == 0 and startPlay:
            startPlay = False
            stopPlay = True

        # Play the audio if needs to be played based on commands and local variables
        if startPlay:
            stream.write(data)
            data = wf.readframes(chunk_size)

    # Closing the pyaudio stream
    stream.close()
    # Closing the wave file
    wf.close()
    #terminating the pyaudio class
    p.terminate()

"""
This function takes input of commands and filename and start playing video using openCV
"""

def playVideo(commands, filename):

    """ Auto stop on these seconds"""
    pauseSeconds = np.array([5, 10, 20, 30])
    
    # This is used to set frames per second in a video usually it will be 30 but based on your video you can change
    framesPerSec = 30
    
    # Making array of exact frames where video needs to be stopped
    # You can replace this array with exact frame numbers if you want to be stopped on specific frame because 1 seconds vides can have mulltiple frames
    pauseFrames = pauseSeconds * framesPerSec

    # Opening video using OpenCV
    cap = cv2.VideoCapture(filename)
    # verifying if the video is opened or not
    if (cap.isOpened() == False):  
        print("Error opening video  file")

    # These two line are used to make the video full screen
    # Uncommect below two lines of code to make video full screen
    # cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
    # cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    
    # Used to save the current frame number
    currentFrameNo = 0
    # counter is used to to pause video after displaying every frame
    counter = 0
    # Run until stopped or video finished
    while cap.isOpened() and commands[1] == 0:
        while commands[0] == 1:
            # Updating the current frame number
            currentFrameNo = currentFrameNo + 1
            # Reading the next frame
            ret, frame = cap.read()
            # Stop when there is no frame to read
            if ret == True:
                # Show the frame using OpenCV
                cv2.imshow('window', frame)
                
                """
                Wait between showing next frame one second has 1000 miliseconds
                If there are 30 frames per second then 1000/30 = 33.33
                You can wait 33 seconds in first frame and 34 milliseconds in next frame and loop it
                Because you cannot use float values in milliseconds for OpenCV
                """
                if counter == 0:
                    # wait for 33 milliseconds and make counter 1 so after next frame it will wait 34 milliseconds
                    counter = 1
                    cv2.waitKey(33)
                elif counter == 1:
                    # wait for 34 milliseconds and make counter 0 so after next frame it will wait 33 milliseconds
                    counter = 0
                    cv2.waitKey(34)
            else:
                # Set the commands to stop the program because video is finished
                commands[1] = 1
                commands[2] = 1
                break
            # Check if current frame number is in pause frames and set the command to pause the audio and video
            if currentFrameNo in pauseFrames:
                commands[0] = 0

    #After finishing everything release the video capture
    cap.release()
    # Destroy all windows which are opened by OpenCV
    cv2.destroyAllWindows()


"""
This program will take input video file and audio file and run both simultaneously.
The code is written for 30fps

Keyboard Inputs:

Stop: s
Pause/Play: space button

This program is using multiprocessing to start two processes one for audio and one for video.
The program use shared memory to control both audio and video process.
"""

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='python-video-player')
    parser.add_argument('--video', type=str, default='./video/karate.mp4')
    parser.add_argument('--audio', type=str, default='./audio/karate.wav')
    args = parser.parse_args()

    # verify video and audio files exists
    assert os.path.isfile(args.video)
    assert os.path.isfile(args.audio)

    """
    I createad a multiprocessing array to share commands between processes
    commands[0] : 0 pause and 1 play the video
    commands[1] : 0 play and 1 stop the video
    commands[2] : 0 run program and 1 stop the program
    """

    commands = multiprocessing.Array('i', range(3))
    # 1 to make it play when program started.
    commands[0] = 1
    # 0 to make it run until finished
    commands[1] = 0
    # 0 to not terminate the program
    commands[2] = 0

    """ Audio process and created and shared the commands and file location """
    audio_pocess = multiprocessing.Process(target=playAudio, args=(commands, args.audio, ))
    audio_pocess.start()
    
    # Audio process take some time to load and start the video
    # You can adjust the time based on your pc configuration
    # For me i have to wait 2 seconds to make audio and video sync
    time.sleep(2)
    
    """ Video process and created and shared the commands and file location """
    video_pocess = multiprocessing.Process(target=playVideo, args=(commands, args.video, ))
    video_pocess.start()


    # This is the function for the keyborad listner
    # Here we will control video based on which key is pressed
    def on_press(key):
        if key != -1:
            # Convert the key to string to compare
            key = str(key)
            
            # When we convert it directly to string.
            # For some keys it has a single quote on both sides like if you press s button it will give you string like this 's'
            if key == "'s'":
                # Update commands to stop the program
                commands[1] = 1
                commands[0] = 0
                commands[2] = 1
            elif key == 'Key.space' and commands[0] == 0:
                # Update command to pause the video
                commands[0] = 1
            elif key == 'Key.space' and commands[0] == 1:
                # Update command to play the video
                commands[0] = 0

    # Used to only start keyboard listener once
    kbListner = True
    
    # Run the program until finished or stoped
    while commands[2] == 0:
        if kbListner:
            # Update it so it won't start again
            kbListner = False
            # Starting keyboard listener
            listener = Listener(on_press=on_press)
            listener.start()

    #terminating the video process
    video_pocess.terminate()
    #terminating the audio process
    audio_pocess.terminate()

