from gpiozero import LED

r = LED(25)
g = LED(12)
b = LED(16)
w = LED(21)


ALL_LEDS = {
    "R": r,
    "G": g,
    "B": b,
    "W": w,
}
