# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 16:32:36 2019

@author: hdysheng
"""

def transfer(numID):
    '''
    A function to transfer number plot ID to original plot ID
    '''
    letter_ = numID%6
    if letter_ == 0:
        letter_ = 6
        num = int((numID-6)/6)+1
    else:
        num     = int(numID/6)+1
    
#    print(letter_)
    if letter_ == 1:
        letter = 'A'
    elif letter_ == 2:
        letter = 'B'
    elif letter_ == 3:
        letter = 'C'
    elif letter_ == 4:
        letter = 'D'
    elif letter_ == 5:
        letter = 'E'
    elif letter_ == 6:
        letter = 'F'
    ID = letter + str(num)
    return ID

def reverse_transfer(ID):
    letter = ID[0]
    number = ID[1]
    if letter is 'A':
        num = 1
    elif letter is 'B':
        num = 2
    elif letter is 'C':
        num = 3
    elif letter is 'D':
        num = 4
    elif letter is 'E':
        num = 5
    elif letter is 'F':
        num = 6
    numID = 6*(int(number)-1) + num
    return numID

