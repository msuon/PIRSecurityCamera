import RPi.GPIO as gpio


class PIR:

    pin = 0
    def __init__(self, pin):
        self.pin = pin
        gpio.setmode(gpio.BOARD)
        gpio.setup(pin, gpio.IN)


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        gpio.cleanup()

    def add_handler(self, func, direction=gpio.RISING):
        gpio.add_event_detect(self.pin, direction, callback=func)


