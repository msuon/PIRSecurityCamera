from time import sleep
import subprocess
import logging
import GDrive
import socket
import PIR
import sys
import os

log_path = "/home/msuon/projects/security-camera-v2/logs/PIRCamrea.log"

TCP_IP = "localhost"
TCP_PORT = 10000
BUFFSIZE = 1024

def send_capture_request():
    MESSAGE = "CAMERA_CAPTURE"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(MESSAGE)

    sleep(0.5)                                              # Sleep for 0.5 seconds for any left over before reading
    data = s.recv(BUFFSIZE)
    s.close()
    return data

def capture_and_send(channel):
    logging.info("Motion Detected! Taking Picture...")
    fileName = send_capture_request()
    GDrive.add_file(fileName, "PIRSecurity_Pictures")
    sleep(.5)

if __name__ == "__main__":
    logging.basicConfig(filename=log_path, level=logging.DEBUG, format='[%(asctime)s]%(levelname)s: %(message)s')

    # Check if instance of program is already running
    pid = str(os.getpid())
    pidfile = "/tmp/PIRSecurityCameraV2.pid"

    if os.path.isfile(pidfile):
        logging.info("Program already running exiting this process...")
        sys.exit()
    with open(pidfile, "w") as f:
        f.write(pid)

    try:
        logging.info("Staring PIR Camera...")

        pir = PIR.PIR(7)
        pir.add_handler(capture_and_send)

        logging.info("PIR Camrea Ready...")
        while True:
            sleep(1)

    finally:
        subprocess.call(["rm {}".format(pidfile)], shell=True)
        logging.warning("Exiting program...")
