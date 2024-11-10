import json
import os
import random
import math
import shutil

# os.makedirs("images/test", exist_ok=True)
# os.makedirs("images/train", exist_ok=True)

# labels = ["M2", "M3", "M4", "M5", "M6", "M7", "M8", "WOOD"]
# for label in labels:
#     folder = "frames/" + label
#     files = []
#     for file_name in os.listdir(folder):
#         im = os.path.join(folder, file_name)
#         # checking if it is a file
#         if os.path.isfile(im):
#             files.append(im)
    
#     random.shuffle(files)
#     for i in range(int(math.ceil(len(files) / 20))):
#         f = files.pop(0)
#         shutil.copyfile(f, "images/test/" + f.split("/")[-1])
    
#     for f in files:
#         shutil.copyfile(f, "images/train/" + f.split("/")[-1])

id = 0
f = open("metadata.jsonl", "r")
out = open("images/metadata.jsonl", "w")
for l in f.readlines():
    d = json.loads(l)
    d["image_id"] = int(d["file_name"].replace(".png", ""))
    if os.path.exists(f"images/test/{d['file_name']}"):
        d["file_name"] = "test/" + d["file_name"]
    else:
        d["file_name"] = "train/" + d["file_name"]
    area = []
    ids = []
    for b in d["objects"]["bbox"]:
        area.append(b[2] * b[3])
        ids.append(id)
        id += 1
    d["objects"]["area"] = area
    d["objects"]["id"] = ids
    out.write(json.dumps(d))
    out.write("\n")