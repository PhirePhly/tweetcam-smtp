#!/usr/bin/env python

import RPi.GPIO as GPIO
from time import sleep

import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

GPIO.setmode(GPIO.BCM)

yellow_led=22
green_led=27
shutter_pin = 17

email_addr_from = 'kenneth@fcix.net'
email_addr_to = 'kennethfinnegan2007@gmail.com'

GPIO.setup (yellow_led, GPIO.OUT)
GPIO.setup (green_led, GPIO.OUT)
GPIO.setup (shutter_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

photo_taken=0

sleep(2)

def take_photo(pin):
    GPIO.output(yellow_led, True)
    sleep(0.1)
    global photo_taken
    photo_taken = 1

    send_email()
    GPIO.output(yellow_led, False)
    sleep(0.1)


def send_email():

    message = MIMEMultipart()
    message['From'] = email_addr_from
    message['To'] = email_addr_to
    message['Date'] = formatdate(localtime=True)
    message['Subject'] = 'Someone pushed a button on the Raspberry Pi!'

    message.attach(MIMEText("Aren't you glad kenneth set your email as the destination address in this script?"))

    smtp = smtplib.SMTP('localhost')
    smtp.sendmail(email_addr_from, email_addr_to, message.as_string())
    smtp.close()




GPIO.add_event_detect(shutter_pin, GPIO.FALLING, callback=take_photo, bouncetime=200)

while True:
    GPIO.output(green_led, True)
    sleep(0.05)
    GPIO.output(green_led, False)
    sleep(2)
    if photo_taken == 1:
        photo_taken = 0
        for x in range(3):
            GPIO.output(green_led, True)
            sleep(0.1)
            GPIO.output(green_led, False)
            sleep(0.1)




GPIO.cleanup(shutter_pin)
GPIO.cleanup(yellow_led)
GPIO.cleanup(green_led)
