import cv2
import os


def take(foldername):
    images = 10  # Number of images to be taken
    ramp_frames = 5
    cap = cv2.VideoCapture(1)
    cap.set(3, 1280)
    cap.set(4, 720)

    os.chdir('/home/samir/danbotsII/folders')
    os.mkdir(foldername)
    os.chdir(foldername)
    # Captures a single image from the camera and returns it in PIL format

    def get_image():
        # read is the easiest way to get a full image out of a VideoCapture object.
        retval, im = cap.read()
        return im

    def capture():
        # Ramp the camera - these frames will be discarded and are only used to allow v4l2
        # to adjust light levels, if necessary
        for j in xrange(ramp_frames):
            get_image()
            # Take the actual image we want to keep
        camera_capture = get_image()
        print("Took image...")
        return camera_capture

    for i in xrange(images):
        image = capture()
        cv2.imshow("take", image)
        myfile = "pose" + str(i) + ".png"
        cv2.imwrite(myfile, image)  # save image to incremented fille name
        cv2.waitKey(0)

    # You'll want to release the camera, otherwise you won't be able to create a new
    # capture object until your script exits
    cap.release()
    cv2.destroyAllWindows()
    return
