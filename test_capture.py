import security_camera

if __name__ == "__main__":
    sc = security_camera.SecurityCamera()
    fn = sc.capture()
    sc.email_picture(fn, "TestImage")
