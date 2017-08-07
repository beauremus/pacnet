from arduino import Arduino

BOARD = Arduino()

while True:
    print(BOARD.get_pin('20'))
