import cv2
import os

cam = cv2.VideoCapture(0)

cv2.namedWindow("test")

img_counter = 322

os.makedirs("frames", exist_ok=True)

labels = ["M2", "M3", "M4", "M5", "M6", "M7", "M8", "WOOD"]
label = 0

for l in labels:
    os.makedirs(f"frames/{l}", exist_ok=True)

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break

    disp = frame.copy()
    font = cv2.FONT_HERSHEY_SIMPLEX

    # org
    org = (200, 200)

    # fontScale
    fontScale = 4
    
    # Blue color in BGR
    color = (255, 0, 0)

    # Line thickness of 2 px
    thickness = 10
    
    # Using cv2.putText() method
    image = cv2.putText(disp, labels[label], org, font, 
                    fontScale, color, thickness, cv2.LINE_AA)

    cv2.imshow("test", disp)

    k = cv2.waitKey(1)
    if k-49 >= 0 and k-49 < 8:
        # 1-8 pressed pressed
        label = k-49
        print(f"Selected label {label} which is {labels[label]}")
    elif k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "frames/{}/{}.png".format(labels[label], img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()
