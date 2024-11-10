import cv2
import numpy as np
from matplotlib import pyplot as plt
import os
import json

labels = ["M2", "M3", "M4", "M5", "M6", "M7", "M8", "WOOD"]
label = 7

f = open("metadata.jsonl", "a")
folder = "frames/" + labels[label]

def click_event(event, x, y, flags, params):
    global click
    global previous
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        previous = click

        click = [x, y]
        if previous != None:
            box = [min(previous[0], click[0]), min(previous[1], click[1]), abs(previous[0] - click[0]), abs(previous[1] - click[1])]
            boxes.append(box)
            label_list.append(label)
            click = None
            previous = None        


# driver function
if __name__ == "__main__":
    # iterate over files in
    # that directory
    for file_name in os.listdir(folder):
        im = os.path.join(folder, file_name)
        # checking if it is a file
        if os.path.isfile(im):
            # reading the image
            org_img = cv2.imread(im, 1)

            click = None
            previous = None
            boxes = []
            label_list = []
            while True:
                img = org_img.copy()
                cv2.setMouseCallback("image", click_event)
                # setting mouse handler for the image
                # and calling the click_event() function

                cv2.putText(img, labels[label], (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 
                    4, (255, 0, 0), 10, cv2.LINE_AA)

                font = cv2.FONT_HERSHEY_SIMPLEX
                if click != None:
                    cv2.putText(img, str(click[0]) + "," + str(click[1]), (click[0], click[1]), font, 1, (255, 0, 0), 2)

                if previous != None:
                    cv2.putText(img, str(previous[0]) + "," + str(previous[1]), (previous[0], previous[1]), font, 1, (255, 0, 0), 2)

                for box, l in zip(boxes, label_list):
                    cv2.rectangle(img,(box[0],box[1]),(box[0]+box[2],box[1]+box[3]),(0,255,0),2)
                    cv2.putText(img, str(l), (box[0], box[1]), font, 1, (255, 0, 0), 2)

                cv2.imshow("image", img)
                    
                k = cv2.waitKey(1)
                if k-49 >= 0 and k-49 < 8:
                    # 1-8 pressed pressed
                    label = k-49
                    print(f"Selected label {label} which is {labels[label]}")
                elif k%256 == 27:
                    # ESC pressed
                    print("Escape hit, closing...")
                    # break
                elif k%256 == 114:
                    boxes = []
                    label_list = []
                    click = None
                    previous = None
                elif k%256 == 32:
                    # SPACE pressed
                    print(boxes, label_list)

                    data = {
                        "file_name": file_name,
                        "objects": {
                            "bbox": boxes,
                            "categories": label_list,
                        },
                    }
                    
                    f.write(json.dumps(data))
                    f.write("\n")
                    break

            # close the window
            cv2.destroyAllWindows()

f.close()