import os
import sys
import json
import time
import socket
import logging
import datetime
import picamera
from threading import Thread

TCP_IP = "localhost"
TCP_PORT = 10000
BUFFER_SIZE = 1024


class socket_camera_thread(Thread):
    def __init__(self,ip, port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port

    def run(self):
        while True:
            data = conn.recv(2048)
            time.sleep(.5)
            if not data:
                break

            if data == "CAMERA_RESTART":
                logging.info("Restarting Camera...")
                camera_module.close()
                start_camera()

            elif data == "CAMERA_CAPTURE":
                logging.info("Taking picture...")
                image_path = capture()
                logging.info("Captured image in {}".format(image_path))
                conn.send(image_path)

def capture():
    file_name = "PiImage_{}.jpg".format(datetime.datetime.now().strftime("%m-%d-%Y_%H-%M-%S"))
    file_path = os.path.join(config["data_save_dir"], file_name)

    logging.info("Taking Picture...")
    camera_module.capture(file_path)
    logging.info("Captured picture in {}".format(file_path))
    return file_path

def start_camera():
    try:
        global camera_module
        camera_module = picamera.PiCamera()
        camera_module.rotation = 180
        time.sleep(2)
        camera_module.exposure_mode = 'sports'
        logging.info("Camera ready...")
    except picamera.PiCameraError:
        logging.error("Problem with initializing PiCamera!")


if __name__ == "__main__":
    # Initialize Logging
    log_path = "/home/msuon/projects/security-camera-v2/logs/socket_camera.log"
    logging.basicConfig(filename=log_path, level=logging.DEBUG, format='[%(asctime)s]%(levelname)s: %(message)s')

    try:
        logging.info("Loading config...")
        CONFIG_PATH = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "config.json"
        )
        with open(CONFIG_PATH, "r") as f:
            config = json.loads(f.read())

        # Setup Image Directory
        if not os.path.isdir(config["data_save_dir"]):
            os.mkdir(config["data_save_dir"])

        logging.info("Starting Up...")
        start_camera()

        # Start up Camera Server
        tcpsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpsocket.bind((TCP_IP, TCP_PORT))
        threads = []

        while True:
            tcpsocket.listen(4)
            (conn, (ip,port)) = tcpsocket.accept()
            new_thread = socket_camera_thread(ip, port)
            new_thread.start()
            threads.append(new_thread)

        for t in threads:
            t.join()
    except IOError:
        logging.error("No config file found...")
    except:
        e = sys.exc_info()[0]
        logging.error(e)
