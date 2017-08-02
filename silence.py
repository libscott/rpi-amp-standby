import subprocess
import time
import RPi.GPIO as GPIO


# $ adduser root pulse-access
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)
GPIO.output(26, 0)

silence = True
delay = 5
lastamp = 0


arecord = subprocess.Popen(
        ['arecord', '-D', 'pulse', '-q', '-r', '2000'],
        stdout=subprocess.PIPE)

print repr(arecord.stdout.read(100))


while True:
    t = time.time()
    p = arecord.stdout.read(1)
    amp = abs(ord(p) - 128)
    if amp > 1:
        if silence:
            silence = False
            GPIO.output(26, 0)
        lastamp = t
    else:
        if not silence:
            if t - lastamp > delay:
                silence = True
                GPIO.output(26, 1)
