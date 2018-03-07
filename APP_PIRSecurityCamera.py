from threading import Thread
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

threads = []

class upload_thread(Thread):
    def __init__(self, file_path):
        Thread.__init__(self)
        self.file_path = file_path

    def run(self):
        logging.info("Uploading to GDrive...")
        GDrive.add_file(self.file_path, "PIRSecurity_Pictures")
        logging.info("Uploaded {}".format(self.file_path))


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
    new_thread = upload_thread(fileName)
    new_thread.start()
    threads.append(new_thread)
    sleep(.5)

if __name__ == "__main__":
    if not os.path.isdir(os.path.dirname(log_path)):
        os.mkdir(os.path.dirname(log_path))
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
        logging.warning("Exiting program...")
        logging.debug("Removing pidfile...")
        subprocess.call(["rm {}".format(pidfile)], shell=True)
        logging.debug("Joining threads...")
        for t in threads:
            t.join()
        logging.info("Program Exited")
