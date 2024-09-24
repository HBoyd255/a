# Harry Boyd - 23/09/2024 - github.com/hboyd255

import cv2

# Flag to use a static image or the camera.
USE_STATIC_IMAGE = False
IMAGE_PATH = "ExampleImages/aruco.png"


def normalise_coords(coords_float):
    x = int(coords_float[0])
    y = int(coords_float[1])
    return x, y


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

        print(corner_tl)

        cv2.circle(marked_image, corner_tl, 5, (255, 0, 0), 3)
        cv2.circle(marked_image, corner_tr, 5, (0, 255, 0), 3)
        cv2.circle(marked_image, corner_br, 5, (0, 0, 255), 3)
        cv2.circle(marked_image, corner_bl, 5, (255, 255, 0), 3)

    # Draw the detected markers on the image.
    frame_markers = cv2.aruco.drawDetectedMarkers(image.copy(), corners, ids)

    # Display the original image.
    cv2.namedWindow("Original Image")
    cv2.namedWindow("Markers")

    # Display the images.
    cv2.imshow("Original Image", image)
    cv2.imshow("Markers", marked_image)


if USE_STATIC_IMAGE:

    image = cv2.imread(IMAGE_PATH)
    process(image)
else:

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    success, img = cap.read()

    while success and cv2.waitKey(1) == -1:
        process(img)
        success, img = cap.read()


cv2.waitKey(0)
cv2.destroyAllWindows()
