# used for mapping the outputs from xbox left stick
from inputs import get_gamepad


x_s = []
y_s = []

def stats():
    print(f"x min,max: {min(x_s)},{max(x_s)}")
    print(f"y min,max: {min(y_s)}, {max(y_s)}")

def main():
    while True:
        events = get_gamepad()
        for event in events:
            if event.ev_type == 'Absolute':
                if event.code == 'ABS_X':
                    print(f"x: {event.state}")
                    x_s.append(event.state)
                elif event.code == 'ABS_Y':
                    print(f"y: {event.state}")
                    y_s.append(event.state)
            if event.ev_type == 'Key' and event.code == 'BTN_SOUTH' and event.state == 1: # pressing A clicks mouse
                stats()
                x_s.clear()
                y_s.clear()
                



if __name__ == '__main__':
    main()
