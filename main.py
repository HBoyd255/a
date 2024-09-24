# Harry Boyd - 23/09/2024 - github.com/hboyd255

import time
import cv2
import libcamera
from picamera2 import Picamera2
import serial

# TODO add a way to read in the com port
COM_PORT = "/dev/ttyACM0"
BAUDRATE = 230400
TIMEOUT = 0.1

# Flag to use a static image or the camera.
USE_STATIC_IMAGE = False
IMAGE_PATH = "ExampleImages/aruco.png"


try:
    ser = serial.Serial(port=COM_PORT, baudrate=BAUDRATE, timeout=TIMEOUT)
except Exception as e:
    raise Exception(f"{COM_PORT} not found.") from e


def normalise_coords(coords_float):
    x = int(coords_float[0])
    y = int(coords_float[1])
    return x, y


def set_velocity(angular_velocity):

    if(angular_velocity > 50):
        angular_velocity = 50

    if(angular_velocity < -50):
        angular_velocity = -50

    ser.write((str(angular_velocity) + "\n").encode("utf-8"))

# Function to process the image, either once from a static image or continuously
# from the camera.
def process(image):

    # Convert the image to grayscale.
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    marked_image = image.copy()

    # Create the aruco detector.
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
    aruco_params = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

    # Detect the markers in the image.
    corners, ids, rejected = detector.detectMarkers(gray_image)

    code_found = len(corners) != 0

    if code_found:

        first_set_of_corners = corners[0][0]

        corner_tl = normalise_coords(first_set_of_corners[0])
        corner_tr = normalise_coords(first_set_of_corners[1])
        corner_br = normalise_coords(first_set_of_corners[2])
        corner_bl = normalise_coords(first_set_of_corners[3])

        centre_x = (corner_tl[0] + corner_br[0]) / 2
        centre_y = (corner_tl[1] + corner_br[1]) / 2

        centre_coords = (int(centre_x), int(centre_y))

        centre_modifier = -int((centre_coords[0] - 200) / 3)

        print(centre_modifier)

        set_velocity(centre_modifier)

        cv2.circle(marked_image, corner_tl, 5, (255, 0, 0), 3)
        cv2.circle(marked_image, corner_tr, 5, (0, 255, 0), 3)
        cv2.circle(marked_image, corner_br, 5, (0, 0, 255), 3)
        cv2.circle(marked_image, corner_bl, 5, (255, 255, 0), 3)

        cv2.circle(marked_image, centre_coords, 5, (0, 0, 0), 3)

    # Display the original image.
    # cv2.namedWindow("Original Image")
    # cv2.namedWindow("Gray Image")
    cv2.namedWindow("Markers")

    # Display the images.
    # cv2.imshow("Original Image", image)
    # cv2.imshow("Gray Image", gray_image)
    cv2.imshow("Markers", marked_image)


picam2 = Picamera2()
config = picam2.create_still_configuration(
    main={"size": (480, 320)},
    lores={"size": (480, 320)},
    transform=libcamera.Transform(vflip=1, hflip=1),
    queue=False,
)
picam2.configure(config)
picam2.set_controls(
    {"ExposureTime": 10000, "AnalogueGain": 5}
)  # Shutter time and analogue signal boost
picam2.start(show_preview=False)

if USE_STATIC_IMAGE:

    image = cv2.imread(IMAGE_PATH)
    process(image)
else:

    # this takes a picture. img can be used with cv2
    captured_image = picam2.capture_array()

    while cv2.waitKey(1) == -1:

        process(captured_image)
        captured_image = picam2.capture_array()
        # this takes a picture. img can be used with cv2


cv2.waitKey(0)
cv2.destroyAllWindows()
picam2.close()  # when you're done taking photos, this closes the camera connection

print("oi")
# set_velocity(30, 0)
