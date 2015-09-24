#!/usr/bin/env python3
# coding: utf8

import RPi.GPIO as GPIO
import configs

if __name__ == "__main__":
    LAMP_PIN = configs.lamp_pin
    SERVO_PIN = configs.servo_pin

    GPIO.setmode(GPIO.BCM)
    # GPIO.cleanup()
    GPIO.setwarnings(False)
    GPIO.setup(LAMP_PIN, GPIO.OUT)  # lamp
    GPIO.setup(SERVO_PIN, GPIO.OUT)  # servo

    GPIO.output(LAMP_PIN, GPIO.LOW)
    GPIO.output(SERVO_PIN, GPIO.LOW)

    GPIO.cleanup()
