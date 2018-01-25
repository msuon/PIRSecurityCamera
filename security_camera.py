import picamera
import os
import json
import datetime
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from time import sleep

class SecurityCamera:

    def __init__(self):
        CONFIG_PATH = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "config.json"
        )
        with open(CONFIG_PATH, "r") as f:
            self.config = json.loads(f.read())

        if not os.path.isdir(self.config["data_save_dir"]):
            os.mkdir(self.config["data_save_dir"])

    def email_picture(self, file_path, subject):
        image_data = open(file_path, "rb").read()

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = self.config["email_from"]
        msg["To"] = self.config["email_to"]
        msg["cc"] = self.config["email_cc"]

        print("Sending Email With Image...")
        print("To: {}".format(msg["To"]))
        print("From: {}".format(msg["From"]))
        print("Subject: {}".format(msg["Subject"]))

        image_attach = MIMEImage(image_data, os.path.basename(file_path))
        msg.attach(image_attach)

        smtplib_server = smtplib.SMTP('localhost')
        smtplib_server.ehlo()
        smtplib_server.starttls()
        smtplib_server.ehlo()

        smtplib_server.sendmail(
            self.config["email_from"],
            self.config["email_to"],
            msg.as_string()
        )
        smtplib_server.quit()
        print("Sending Complete!")

    def capture(self):
        file_name = "PiImage_{}.jpg".format(datetime.datetime.now().strftime("%m-%d-%Y_%H-%M-%S"))
        file_path = os.path.join(self.config["data_save_dir"], file_name)

        c = picamera.PiCamera()
        c.rotation = 180
        sleep(2)
        print "Taking Picture..."
        c.capture(file_path)
        c.close()
        return file_path

    def save(self):
        print("save image")




