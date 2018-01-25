import PIR
from time import sleep



def handler():
    print "detection!..."

if __name__ == "__main__":
    x = PIR.PIR(7)
    x.add_handler(handler)

    while True:
        sleep(1)