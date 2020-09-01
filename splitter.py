# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 11:47:50 2020

@author: Muhammad Abid
"""
import os
import argparse
import moviepy.editor as mp

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='python-video-splitter')
    parser.add_argument('--video', type=str, default='./video/karate.mp4')
    parser.add_argument('--audio', type=str, default='./audio/karate.wav')
    args = parser.parse_args()

    # verify video and audio files exists
    assert os.path.isfile(args.video)

    # Read the video file from the given location 
    clip = mp.VideoFileClip(args.video) 
	  
    # Save the audio to local give path
    clip.audio.write_audiofile(args.audio) 
