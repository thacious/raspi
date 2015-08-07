#!/usr/bin/env python

#Imports
from Tkinter import *
import time
import tkMessageBox
import RPi.GPIO as GPIO
import Tkinter
from imapclient import IMAPClient


#GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GREEN_LED = 18
RED_LED = 23
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)


#Window Config
root = Tkinter.Tk()
root.title("LED Project Controller")
#root.geometry("640x480")


#Frames
blinkFrame = LabelFrame(root, text="Blink Timer", bg="white", relief=RAISED, bd=3, padx=5, pady=5)
blinkFrame.grid(row=0, column=0, padx=10, pady=10)
mailFrame = LabelFrame(root, text="Mail Indicator", bg="white", relief=RAISED, bd=3, padx=5, pady=5)
mailFrame.grid(row=0, column=1, padx=10, pady=10)
rgFrame = LabelFrame(root, text="Light Control", bg="white", relief=RAISED, bd=3, padx=5, pady=5)
rgFrame.grid(row=1, column=0,padx=10, pady=10)
mcFrame = LabelFrame (root, text="Morse Code Flasher", bg="white", relief=RAISED, bd=3, padx=5, pady=5)
mcFrame.grid(row=1, column=1, padx=10, pady=10)


#Blinker
blinkLbl = Label(blinkFrame, text="How Many Seconds Should the Lights Blink?")
blinkLbl.grid(row=0, padx=5, pady=5)

blinkEntry = Entry(blinkFrame, bd =1)
blinkEntry.grid(row=1, padx=5, pady=5)

def Blink():
    i = int(blinkEntry.get())

    while (i > 0):
        blinkTxt.insert(END, str(i) + "\n")
        GPIO.output(GREEN_LED, True)
        GPIO.output(RED_LED, False)
        time.sleep(1)
        i = i - 1
        blinkTxt.insert(END, str(i) + "\n")
        GPIO.output(GREEN_LED, False)
        GPIO.output(RED_LED, True)
        time.sleep(1)
        i = i - 1

blinkBttn = Tkinter.Button(blinkFrame, text="BLINK", command=Blink)
blinkBttn.grid(row=3, padx=10,pady=20)

blinkTxt = Text(blinkFrame, height=10, width=40, bg="black", fg="white")
blinkTxt.grid(row=5, padx=5, pady=5)


#Mail Indicator
unLbl = Label(mailFrame, text="Username")
unLbl.pack(padx=5, pady=5)
unEntry = Entry(mailFrame, bd=1)
unEntry.pack(padx=5, pady=5)

pwLbl = Label(mailFrame, text="Password")
pwLbl.pack(padx=5, pady=5)
pwEntry = Entry(mailFrame, bd=1, show="*")
pwEntry.pack(padx=5, pady=5)

def Check():
    HOSTNAME = 'imap.gmail.com'
    USERNAME = unEntry.get()
    PASSWORD = pwEntry.get()
    MAILBOX = 'Inbox'
    NEWMAIL_OFFSET = 0

    server = IMAPClient(HOSTNAME, use_uid=True, ssl=True)
    server.login(USERNAME, PASSWORD)

    login = 'Logging in as ' + USERNAME + '\n'
    mailTxt.insert(INSERT, login)
    select_info = server.select_folder(MAILBOX)
    inboxcount = '%d messages in INBOX \n' % select_info['EXISTS']
    mailTxt.insert(INSERT, inboxcount)

    folder_status = server.folder_status(MAILBOX, 'UNSEEN')
    newmails = int(folder_status['UNSEEN'])

    newmail = "You have " + str(newmails) + " new emails\n"
    mailTxt.insert(INSERT, newmail)

    if newmails > NEWMAIL_OFFSET:
        GPIO.output(GREEN_LED, True)
        GPIO.output(RED_LED, False)
    else:
        GPIO.output(GREEN_LED, False)
        GPIO.output(RED_LED, True)
  
mailBttn = Tkinter.Button(mailFrame, text="Check Mail", command=Check)
mailBttn.pack(padx=10, pady=20)

mailTxt = Text(mailFrame, height=10, width=40, bg="black", fg="white")
mailTxt.pack(padx=5, pady=5)


#Red Light/Green Light
def RedOn():
    GPIO.output(RED_LED, True)
    rgTxt.insert(INSERT, "The Red Light is On\n")

def RedOff():
    GPIO.output(RED_LED, False)
    rgTxt.insert(INSERT, "The Red Light is Off\n")

def GreenOn():
    GPIO.output(GREEN_LED, True)
    rgTxt.insert(INSERT, "The Green Light is On\n")

def GreenOff():
    GPIO.output(GREEN_LED, False)
    rgTxt.insert(INSERT, "The Green Light is Off\n")

rOn = Tkinter.Button(rgFrame, text="Red Light On", command=RedOn)
rOff = Tkinter.Button(rgFrame, text="Red Light Off", command=RedOff)
gOn = Tkinter.Button(rgFrame, text="Green Light On", command=GreenOn)
gOff = Tkinter.Button(rgFrame, text="Green Light Off", command=GreenOff)

rOn.grid(row=0, column=0, padx=5, pady=5)
rOff.grid(row=1, column=0, padx=5, pady=5)
gOn.grid(row=2, column=0, padx=5, pady=5)
gOff.grid(row=3, column=0, padx=5, pady=5)

rgTxt = Text(rgFrame, height=10, width=40, bg="black", fg="white")
rgTxt.grid(row=5, padx=5, pady=5)


#Morse Code
mcLbl = Label(mcFrame, text="Enter Your Message", padx=5, pady=5)
mcLbl.grid(row=0, padx=5, pady=5)

mcEntry = Entry(mcFrame, bd=1)
mcEntry.grid(row=1, padx=5, pady=5)

CODE = {' ': ' ',
        "'": '.----.',
        '(': '-.--.-',
        ')': '-.--.-',
        ',': '--..--',
        '-': '-....-',
        '.': '.-.-.-',
        '/': '-..-.',
        '0': '-----',
        '1': '.----',
        '2': '..---',
        '3': '...--',
        '4': '....-',
        '5': '.....',
        '6': '-....',
        '7': '--...',
        '8': '---..',
        '9': '----.',
        ':': '---...',
        ';': '-.-.-.',
        '?': '..--..',
        'A': '.-',
        'B': '-...',
        'C': '-.-.',
        'D': '-..',
        'E': '.',
        'F': '..-.',
        'G': '--.',
        'H': '....',
        'I': '..',
        'J': '.---',
        'K': '-.-',
        'L': '.-..',
        'M': '--',
        'N': '-.',
        'O': '---',
        'P': '.--.',
        'Q': '--.-',
        'R': '.-.',
        'S': '...',
        'T': '-',
        'U': '..-',
        'V': '...-',
        'W': '.--',
        'X': '-..-',
        'Y': '-.--',
        'Z': '--..',
        '_': '..--.-'}

def dot():
    GPIO.output(GREEN_LED, True)
    time.sleep(0.2)
    GPIO.output(GREEN_LED, False)
    time.sleep(0.2)

def dash():
    GPIO.output(GREEN_LED, True)
    time.sleep(0.5)
    GPIO.output(GREEN_LED, False)
    time.sleep(0.2)

def encode():
    message = mcEntry.get()
    for letter in message:
        for symbol in CODE[letter.upper()]:
            if symbol == '-':
                dash()
            elif symbol == '.':
                dot()
            else:
                time.sleep(0.5)
    mcTxt.insert(INSERT, "Message Transmitted\n")
    GPIO.output(RED_LED, True)
 
mcBttn = Tkinter.Button(mcFrame, text="Flash Message", command=encode)
mcBttn.grid(row=3, padx=5, pady=5)

mcTxt = Text(mcFrame, height=10, width=40, bg="black", fg="white")
mcTxt.grid(row=5, padx=5, pady=5)
    
root.mainloop()