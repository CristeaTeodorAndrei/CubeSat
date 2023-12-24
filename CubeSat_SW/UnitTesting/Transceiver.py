import spidev
import RPi.GPIO as GPIO
from nRF24 import *

# Setări pinuri NRF24L01
CE_PIN = 8
CSN_PIN = 25

# Inițializare NRF24L01
radio = NRF24()
radio.begin(0, 0, CE_PIN, CSN_PIN)  # canal 0, adresa 0

# Setare putere de transmisie și viteză de date
radio.setPALevel(RF24_PA_HIGH)
radio.setDataRate(RF24_250KBPS)

# Adresa destinatarului
address = [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]

def setup():
    # Inițializare GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CE_PIN, GPIO.OUT)
    GPIO.setup(CSN_PIN, GPIO.OUT)
    GPIO.output(CE_PIN, GPIO.LOW)
    GPIO.output(CSN_PIN, GPIO.LOW)

def loop():
    while True:
        message = input("Introdu mesajul: ")
        sendMessage(message)

def sendMessage(message):
    # Setare adresa de transmisie
    radio.openWritingPipe(address)

    # Activare transmitator
    GPIO.output(CE_PIN, GPIO.HIGH)

    # Trimitere mesaj
    radio.write(message)

    # Dezactivare transmitator
    GPIO.output(CE_PIN, GPIO.LOW)

if __name__ == "__main__":
    try:
        setup()
        loop()
    except KeyboardInterrupt:
        GPIO.cleanup()