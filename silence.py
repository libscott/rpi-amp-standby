import subprocess
import time
import RPi.GPIO as GPIO

GPIO_CHANNEL = 26

# $ adduser root pulse-access
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_CHANNEL, GPIO.OUT)

arecord = subprocess.Popen(
        ['arecord', '-D', 'pulse', '-q', '-r', '2000'],
        stdout=subprocess.PIPE)

time.sleep(1)
print repr(arecord.stdout.read(100))

silence = GPIO.input(GPIO_CHANNEL)
delay = 20
lastamp = time.time()

while True:
    t = time.time()
    p = arecord.stdout.read(1)
    amp = abs(ord(p) - 128)
    if amp > 1:
        if silence:
            silence = False
            GPIO.output(GPIO_CHANNEL, 0)
        lastamp = t
    else:
        if not silence:
            if t - lastamp > delay:
                silence = True
                GPIO.output(GPIO_CHANNEL, 1)
