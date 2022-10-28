#controlling mouse from xbox controller, hardcoded to hell

from pynput.mouse import Button, Controller
from inputs import get_gamepad
import inputs

mouse = Controller()
gamepad = inputs.devices.gamepads[0]

def click():
    mouse.press(Button.left)
    mouse.release(Button.left)

def hold_click():
    mouse.press(Button.left)

def move_mouse(direction, speed):   
    if direction == 'a':
        mouse.position = (mouse.position[0], mouse.position[1] - speed)
    elif direction == 'b':
        mouse.position = (mouse.position[0] + speed, mouse.position[1] - speed)
    elif direction == 'c':
        mouse.position = (mouse.position[0] + speed, mouse.position[1])
    elif direction == 'd':
        mouse.position = (mouse.position[0] + speed, mouse.position[1] + speed)
    elif direction == 'e':
        mouse.position = (mouse.position[0], mouse.position[1] + speed)
    elif direction == 'f':
        mouse.position = (mouse.position[0] - speed, mouse.position[1] + speed)
    elif direction == 'g':
        mouse.position = (mouse.position[0] - speed, mouse.position[1])
    elif direction == 'h':
        mouse.position = (mouse.position[0] - speed, mouse.position[1] - speed)

def axis_ranges(x, y): # big cringe
    if -2283 <= x <= 11520 and -11190 <= y <= 5267: #null area
        return 'null'
    elif -24092 <= x <= 20123 and 29437<= y <= 32767: #A
        return 'a'
    elif 6526 <= x <= 32767 and 12150 <= y <= 32767: #B
        return 'b'
    elif 32225 <= x <= 32767 and -18640 <= y <= 12878: #C
        return 'c'
    elif 9734 <= x <= 32767 and -32768 <= y <= -14415: #D
        return 'd'
    elif -19396 <= x <= 15027 and -32768 <= y <= -31243: #E
        return 'e'
    elif -32170 <= x <= -16570 and -32768 <= y <= -9904: #F
        return 'f'
    elif -32768 <= x <= -29570 and -18911 <= y <= 22568: #G
        return 'g'
    elif -29981 <= x <= -9929 and 19411 <= y <= 32767: #H
        return 'h'

coordsX = [0]
coordsY = [0]

def main():

    while True:
        events = get_gamepad()
        for event in events:
            if event.ev_type == 'Key' and event.code == 'BTN_SOUTH' and event.state == 1: # pressing A clicks mouse
                click()
            if event.ev_type == 'Key' and event.code == 'BTN_WEST' and event.state == 1:  # Pressing X holds left click down
                hold_click()
            if event.ev_type == 'Absolute':
                if event.code == 'ABS_X':
                    coordsX.append(event.state)
                elif event.code == 'ABS_Y':
                    coordsY.append(event.state)
                    
                if event.code == 'ABS_HAT0Y':
                    if event.state == 1:
                        move_mouse('e', 10)
                    elif event.state == -1:
                        move_mouse('a', 10)
                elif event.code == 'ABS_HAT0X':
                    if event.state == 1:
                        move_mouse('c', 10)
                    elif event.state == -1:
                        move_mouse('g', 10)
                    
                if coordsX and coordsY:
                    move_mouse(axis_ranges(coordsX[-1], coordsY[-1]), 7)



if __name__ == '__main__':
    main()
