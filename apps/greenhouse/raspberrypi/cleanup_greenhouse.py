#!/usr/bin/env python3
# coding: utf8

import RPi.GPIO as GPIO
import configs

if __name__ == "__main__":
    GREEN_LED_PIN = configs.green_led_pin
    YELLOW_LED_PIN = configs.yellow_led_pin
    RED_LED_PIN = configs.red_led_pin
    LAMP_PIN = configs.lamp_pin
    SERVO_PIN = configs.servo_pin

    GPIO.setmode(GPIO.BCM)
    # GPIO.cleanup()
    GPIO.setwarnings(False)
    GPIO.setup(YELLOW_LED_PIN, GPIO.OUT)  # yellow led
    GPIO.setup(RED_LED_PIN, GPIO.OUT)  # red led
    GPIO.setup(GREEN_LED_PIN, GPIO.OUT)  # green led
    GPIO.setup(LAMP_PIN, GPIO.OUT)  # lamp
    GPIO.setup(SERVO_PIN, GPIO.OUT)  # servo

    GPIO.output(YELLOW_LED_PIN, GPIO.LOW)
    GPIO.output(RED_LED_PIN, GPIO.LOW)
    GPIO.output(GREEN_LED_PIN, GPIO.LOW)
    GPIO.output(LAMP_PIN, GPIO.LOW)
    GPIO.output(SERVO_PIN, GPIO.LOW)

    GPIO.cleanup()
