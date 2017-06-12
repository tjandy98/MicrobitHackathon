from microbit import *
import random
from microbit import i2c, Image
import music

point=0
direction=0
timer=1000
tune = ["C4:1"]

OLED_ADDR = 0x3c
oled_screen = bytearray('b\x40') + bytearray(512)

def oled_initialize():

    for c in ([0xae], [0xa4], [0xd5, 0xf0], [0xa8, 0x3f], [0xd3, 0x00], [0 | 0x0], [0x8d, 0x14], [0x20, 0x00], [0x21, 0, 127], [0x22, 0, 63], [0xa0 | 0x1], [0xc8], [0xda, 0x12], [0x81, 0xcf], [0xd9, 0xf1], [0xdb, 0x40], [0xa6], [0xd6, 1], [0xaf]):
        i2c.write(OLED_ADDR, b'\x00' + bytearray(c))

def oled_set_pos(col=0, page=0):
    i2c.write(OLED_ADDR, b'\x00' + bytearray([0xb0 | page]))
    c1, c2 = col * 2 & 0x0F, col >> 3
    i2c.write(OLED_ADDR, b'\x00' + bytearray([0x00 | c1]))
    i2c.write(OLED_ADDR, b'\x00' + bytearray([0x10 | c2]))

def oled_clear_screen(c=0):
    global oled_screen
    oled_set_pos()
    for i in range(1, 513):
        oled_screen[i] = 0
    oled_draw_screen()

def oled_draw_screen():
    global oled_screen
    oled_set_pos()
    i2c.write(OLED_ADDR, oled_screen)

def oled_add_text(x, y, text):
    global oled_screen
    for i in range(0, min(len(text), 12 - x)):
        for c in range(0, 5):
            col = 0
            for r in range(1, 6):
                p = Image(text[i]).get_pixel(c, r - 1)
                col = col | (1 << r) if (p != 0) else col
            ind = x * 10 + y * 128 + i * 10 + c * 2 + 1
            oled_screen[ind], oled_screen[ind + 1] = col, col
    oled_set_pos(x * 5, y)
    ind0 = x * 10 + y * 128 + 1
    i2c.write(OLED_ADDR, b'\x40' + oled_screen[ind0 : (ind+1)])

oled_initialize()
oled_clear_screen()
oled_add_text(0,0,'Game Start!')
music.play(music.POWER_UP)

while True:
    display.clear()
    sleep(50)
    direction = random.randrange(0,4)
    sleep(timer)
    if timer > 350:
        timer -=50
    if direction == 0:
       display.show(Image.ARROW_W)
       sleep(timer)
       if pin2.is_touched:
           reading = pin2.read_analog()
           if reading > 100 and reading < 150:
               point +=1
               music.play(tune)
               continue
           else:
               display.show(Image.NO)
               break
    elif direction == 1:
       display.show(Image.ARROW_E)
       sleep(timer)
       if pin2.is_touched:
           reading = pin2.read_analog()
           if reading > 10 and reading < 60:
               point +=1
               music.play(tune)
               continue
           else:
               display.show(Image.NO)
               break
    elif direction == 2:
       display.show(Image.ARROW_N)
       sleep(timer)
       if pin2.is_touched:
           reading = pin2.read_analog()
           if reading < 10:
               point +=1
               music.play(tune)
               continue
           else:
               display.show(Image.NO)
               break
    else:
       display.show(Image.ARROW_S)
       sleep(timer)
       if pin2.is_touched:
           reading = pin2.read_analog()
           if reading > 60 and reading < 100:
               point +=1
               music.play(tune)
               continue
           else:
               display.show(Image.NO)
               break
sleep(1000)


oled_initialize()
oled_clear_screen()

# Screen divided into 12 columns and 4 rows

oled_add_text(0, 0, 'Game over!')
oled_add_text(0,1, 'Point : ' + str(point))
music.play(music.POWER_DOWN)