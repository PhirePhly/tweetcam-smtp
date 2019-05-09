#!/usr/bin/env python

import RPi.GPIO as GPIO
from picamera import PiCamera
from time import sleep

import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

import configparser
import random
from datetime import datetime


GPIO.setmode(GPIO.BCM)

# These are GPIO labels (BCM numbering) as opposed to header pin numbering
record_led=22
heartbeat_led=27
shutter_pin = 17
timer_enable = 18

config = configparser.ConfigParser()
config.read('/etc/tweetcam.conf')

GPIO.setup (record_led, GPIO.OUT)
GPIO.setup (heartbeat_led, GPIO.OUT)
GPIO.setup (shutter_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup (timer_enable, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.output(record_led, False)
GPIO.output(heartbeat_led, False)

photo_taken=0

camera = PiCamera()
camera.resolution = (2560, 1920)
camera.start_preview()

sleep(2)

def take_photo(pin):
    global photo_taken

    # Check the timer switch to decide to sleep a little first
    if (GPIO.input(timer_enable) == GPIO.LOW):
        for x in range(3):
            GPIO.output(record_led, True)
            sleep(0.75)
            GPIO.output(record_led, False)
            sleep(0.75)
        for x in range(3):
            GPIO.output(record_led, True)
            sleep(0.1)
            GPIO.output(record_led, False)
            sleep(0.1)
        

    photoid = datetime.today().strftime('%Y%m%d%H%M%S') + "-" + str(random.randint(10000000,99999999)) + '.jpg'
    photodir = config['TWEETCAM']['photo_directory']
    photo_filename = photodir + photoid

    # Take the actual photo and save it to our photo directory
    camera.capture(photo_filename)

    GPIO.output(heartbeat_led, True)
    photo_taken += 1

    GPIO.output(record_led, True)
    send_email(photofile=photodir+photoid)
    GPIO.output(record_led, False)


def send_email(photofile=None):

    message = MIMEMultipart()
    message['From'] = config['TWEETCAM']['email_addr_from']
    message['To'] = config['TWEETCAM']['email_addr_to']
    message['Date'] = formatdate(localtime=True)
    message['Subject'] = config['TWEETCAM']['message_subject']

    message.attach(MIMEText(config['TWEETCAM']['message_body']))

    if photofile != None:
        with open(photofile, "rb") as openfile:
            message_part = MIMEApplication(openfile.read(), Name=basename(photofile))
        message_part['Content-Disposition'] = 'attachment; filename="%s"' % basename(photofile)
        message.attach(message_part)

    smtp = smtplib.SMTP('localhost')
    smtp.sendmail(config['TWEETCAM']['email_addr_from'], config['TWEETCAM']['email_addr_to'], message.as_string())
    smtp.close()




GPIO.add_event_detect(shutter_pin, GPIO.FALLING, callback=take_photo, bouncetime=200)

heartbeat_pulse = 0

while True:
    heartbeat_pulse = (heartbeat_pulse + 1) % 25
    if heartbeat_pulse == 0:
        GPIO.output(heartbeat_led, True)
        sleep(0.05)
    else:
        GPIO.output(heartbeat_led, False)
        sleep(0.2)
    if photo_taken > 0:
        photo_taken -= 1
        for x in range(3):
            GPIO.output(heartbeat_led, True)
            sleep(0.1)
            GPIO.output(heartbeat_led, False)
            sleep(0.1)




GPIO.cleanup(shutter_pin)
GPIO.cleanup(timer_enable)
GPIO.cleanup(record_led)
GPIO.cleanup(heartbeat_led)
