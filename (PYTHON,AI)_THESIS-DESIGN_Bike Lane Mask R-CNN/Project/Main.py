import cv2
from _CustomLibraries.Detectron2 import Detector
from _CustomLibraries.ResizeWithAspectRatio import ResizeWithAspectRatio
from _CustomLibraries.Distance_Formula import Distance_Formula
from _CustomLibraries.Draw import Draw_Region

# Settings
video_name = "Videos/Shaw blvd Christian Route 2_NVR 160.11_NVR 160.11_20220321075959_20220321080750_617095317.mp4"
window_name = "CCTV_Bike Lane Mask R-CNN"
radius = 10
resize_width = 640
max_radius = 100
default_color = (0, 255, 0)  # BGR
violation_color = (0, 0, 255)  # BGR

# Classes
classes = ["bicycle", "car", "motorcycle", "bus", "truck"]
exclude_class = "bicycle"  # will not marked by violation color

# Global Variables
is_adding_regions = False
frame = None
drawings = []
regions = []


def region_drawing_callback(event, x, y, flags, param):
    global frame, drawings, regions
    radius = cv2.getTrackbarPos("Radius", window_name)
    if event == cv2.EVENT_LBUTTONDOWN:
        drawings.append(frame)
        regions.append(
            {
                "position": (x, y),
                "radius": radius,
            }
        )
        frame = Draw_Region(frame, (x, y), radius)


def draw_detection(frame, class_names_boxes):
    for detected_object in class_names_boxes:
        if detected_object["class_name"] in classes:
            # convert positions to integer
            x1, y1, x2, y2 = [int(integer) for integer in detected_object["boxes"]]
            # get centroid of each boxes
            object_center = (int((x1 + x2) / 2), int((y1 + y2) / 2))
            color = default_color  # BGR: default color green
            violation_text = ""
            if detected_object["class_name"] != exclude_class:
                for region in regions:
                    circle_center = region["position"]
                    radius = region["radius"]
                    if Distance_Formula(circle_center, object_center, radius):
                        color = violation_color
                        violation_text = " : " + "Violation!"
                        break
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 1)
            cv2.circle(frame, object_center, 2, (255, 0, 0), -1)  # check center of each
            cv2.putText(
                frame,
                detected_object["class_name"] + violation_text,
                (x1, y1 - 2),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.3,
                color,
                1,
            )


def get_frame(cap):
    result, frame = cap.read()
    frame = ResizeWithAspectRatio(frame, width=resize_width)
    return result, frame


def start(cap):
    global is_adding_regions, frame, drawings, regions
    # Initialize Detectron2
    detector = Detector(model_type="IS", threshold=0.5, use_gpu=True)
    while cap.isOpened():
        # get first frame for region adding
        if frame is None:
            result, frame = get_frame(cap)
            if not result:
                break
            is_adding_regions = True
        if not is_adding_regions:
            result, original_frame = get_frame(cap)
            frame = original_frame.copy()
            if not result:
                break
            # draw regions for each succeeding frames
            for region in regions:
                circle_center = region["position"]
                radius = region["radius"]
                frame = Draw_Region(frame, circle_center, radius)
            # use original frame for detection
            _detected_image, class_names_boxes = detector.on_image(original_frame)
            draw_detection(frame, class_names_boxes)
        # display the resulting frame
        cv2.imshow(window_name, frame)
        # wait for keypress
        key = cv2.waitKey(1)
        # ESC to quit
        if key & 0xFF == 27:
            break
        if is_adding_regions:
            # drawing mode label
            text = "Drawing Mode"
            cv2.putText(frame, text, (0, 20), 0, 0.75, (0, 0, 0), 3)
            cv2.putText(frame, text, (0, 20), 0, 0.75, (255, 255, 255), 1)
            # check if there's a region created already
            if len(drawings) != 0 or len(regions) != 0:
                # CTRL-Z to undo drawing
                if key & 0xFF == 26:
                    frame = drawings[-1]
                    drawings.pop()
                    regions.pop()
                # ENTER to start detecting
                if key & 0xFF == 13:
                    is_adding_regions = False
                    print("Initialize detection!")
                    cv2.setMouseCallback(window_name, lambda *args: None)


if __name__ == "__main__":
    # initialize cv2 settings
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 1280, 720)
    cv2.setMouseCallback(window_name, region_drawing_callback)
    cv2.createTrackbar("Radius", window_name, 10, max_radius, lambda *args: None)
    # start VideoCapture
    cap = cv2.VideoCapture(video_name)
    start(cap)
    # when everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
