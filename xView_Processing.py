import aug_util as aug
import wv_util as wv
import rectangle as rect
import matplotlib.pyplot as plt
import numpy as np
import csv
from PIL import Image

def image_execute(chip_name):
    #Load an prediction
    f = open("predictions.txt")
    lines = f.readlines()
    for i in range(len(lines)):
        lines[i]=lines[i].split()
    
    #Load an image
    arr = wv.get_image(chip_name)

    #Loading our labels
    coords, chips, classes = wv.get_labels('xView_train.geojson')
    
    #We only want to coordinates and classes that are within our chip
    coords = coords[chips==chip_name]
    classes = classes[chips==chip_name].astype(np.int64)

    #Load the class number -> class string label map
    labels = {}
    with open('xview_class_labels.txt') as f:
        for row in csv.reader(f):
            labels[int(row[0].split(":")[0])] = row[0].split(":")[1]

    """
    intersection = []

    for i in range(len(lines)):
            if float(lines[i][5]) > 0.5:
                xmin = int(lines[i][0])
                ymin = int(lines[i][1])
                xmax = int(lines[i][2])
                ymax = int(lines[i][3])
                temp = rect.Rectangle(xmin,ymin,xmax,ymax)
                for j in range(len(c_box[0])):
                    txmin,tymin,txmax,tymax = c_box[0][j]
                    t_temp = rect.Rectangle(txmin,tymin,txmax,tymax)
                    if t_temp.intersects(temp) == True:
                        inter = t_temp.intersect(temp)
                        if inter.area() > (0.5*temp.area()):
                            position = []
                            position.append(inter.coords[0])
                            position.append(inter.coords[1])
                            position.append(inter.coords[2])
                            position.append(inter.coords[3])
                            intersection.append(position)    
    """

    labelled1 = aug.draw_groundtruth(arr,coords)
    labelled1.save("groundtruth.tif")

    labelled2 = aug.draw_predict(arr,lines)
    labelled2.save("predict.tif")

    blend_img = Image.blend(labelled1, labelled2, 0.3)
    blend_img.save("blend.tif")

