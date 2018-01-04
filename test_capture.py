import security_camera
import GDrive

if __name__ == "__main__":
    sc = security_camera.SecurityCamera()
    fn = sc.capture()
    sc.email_picture(fn, "TestImage")
    GDrive.add_file(fn, "security_images")
