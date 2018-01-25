import security_camera
from time import sleep
import logging
import GDrive
import PIR
import subprocess
import sys
import os

sc = None
log_path = "/home/msuon/projects/security-camera/logs/PIRCamrea.log"
def capture_and_send(channel):
    logging.info("Motion Detected! Taking Picture...")
    fileName = sc.capture()
    sc.email_picture(fileName, "TestPIRImage")
    GDrive.add_file(fileName, "PIRSecurity_Pictures")

if __name__ == "__main__":
    logging.basicConfig(filename=log_path, level=logging.DEBUG, format='[%(asctime)s]%(levelname)s: %(message)s')

    # Check if instance of program is already running
    pid = str(os.getpid())
    pidfile = "/tmp/PIRSecurityCamera.pid"

    if os.path.isfile(pidfile):
        logging.info("Program already running exiting this process...")
        sys.exit()

    with open(pidfile, "w") as f:
        f.write(pid)

    try:
        logging.info("Staring PIR Camera...")
        sc = security_camera.SecurityCamera()

        pir = PIR.PIR(7)
        pir.add_handler(capture_and_send)

        logging.info("PIR Camrea Ready...")
        while True:
            sleep(1)

    finally:
        subprocess.call(["rm {}".format(pidfile)], shell=True)
        logging.warning("Exiting program...")
