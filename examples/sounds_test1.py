#!/usr/bin/env python
# coding=utf-8
# ======== 音声テスト用 =========

import pygame.mixer
import time



pygame.mixer.init()
pygame.mixer.music.load('/home/pi/project1/sounds/knock.wav')
pygame.mixer.music.play(1) # loop count

time.sleep(2)  #10秒再生
pygame.mixer.music.stop()  #停止
pygame.mixer.quit() #音源への電源停止：サーってノイズを消す


pygame.mixer.init()
pygame.mixer.music.load('/home/pi/project1/sounds/start.wav')
pygame.mixer.music.play(1) # loop count

time.sleep(2)  #10秒再生
pygame.mixer.music.stop()  #停止
pygame.mixer.quit() #音源への電源停止：サーってノイズを消す


pygame.mixer.init()
pygame.mixer.music.load('/home/pi/project1/sounds/chime.mp3')
pygame.mixer.music.play(1) # loop count

time.sleep(2)  #10秒再生
pygame.mixer.music.stop()  #停止
pygame.mixer.quit() 