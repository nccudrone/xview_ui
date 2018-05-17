
# coding: utf-8

# In[1]:


import aug_util as aug
import wv_util as wv
import rectangle as rect
import matplotlib.pyplot as plt
import numpy as np
import csv
from PIL import Image

#get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:

def image_execute(file_name):
    #Load an prediction
    f = open("predictions.txt")
    lines = f.readlines()
    for i in range(len(lines)):
        lines[i]=lines[i].split()
    #print(len(lines))


    # In[3]:


    #Load an image
    chip_name = file_name
    #file_name = '5.tif'
    arr = wv.get_image(file_name)

    #plt.figure(figsize=(10,10))
    #plt.axis('off')
    #plt.imshow(arr)


    # In[4]:


    #Loading our labels
    coords, chips, classes = wv.get_labels('xView_train.geojson')
    #We only want to coordinates and classes that are within our chip
    coords = coords[chips==chip_name]
    classes = classes[chips==chip_name].astype(np.int64)


    # In[5]:


    #Load the class number -> class string label map
    labels = {}
    with open('xview_class_labels.txt') as f:
        for row in csv.reader(f):
            labels[int(row[0].split(":")[0])] = row[0].split(":")[1]


    # In[6]:


    #Load the class number -> class string label map
    #colors = {}
    #with open('xview_class_color.txt') as f:
    #    for row in csv.reader(f):
    #        colors[int(row[0].split(":")[0])] = row[0].split(":")[1]


    # In[7]:


    #We can find which classes are present in this image
    #print([colors[i] for i in np.unique(classes)])


    # In[8]:


    #We can chip the image into 500x500 chips
    c_img, c_box, c_cls = wv.chip_image(img = arr, coords= coords, classes=classes, shape=(arr.shape[1],arr.shape[0]))
    #print("Num Chips: %d" % c_img.shape[0])


    # In[9]:


    '''We can plot some of the chips
    fig,ax = plt.subplots(3)
    fig.set_figheight(5)
    fig.set_figwidth(5)

    for k in range(9):
        plt.subplot(3,3,k+1)
        plt.axis('off')
        plt.imshow(c_img[np.random.choice(range(c_img.shape[0]))])

    plt.show()'''


    # In[10]:


    #c_cls[0].size


    # In[11]:


    #c_color=["" for i in range(c_cls[0].size)]
    #for i in range(c_cls[0].size):
    #    c_color[i]=colors[c_cls[0][i]]
    #    print(c_color[i])


    # In[12]:


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
    #print(intersection)      
    """


    # In[13]:


    #We can visualize the chips with their labels
    #ind = np.random.choice(range(c_img.shape[0]))
    #labelled = aug.draw_bboxes(c_img[ind],c_box[ind],lines,intersection)

    #plt.figure(figsize=(30,30))
    #plt.axis('off')
    #plt.imshow(labelled)
    #labelled.save("result.tif")


    # In[14]:


    ind1 = np.random.choice(range(c_img.shape[0]))
    labelled1 = aug.draw_groundtruth(c_img[ind1],c_box[ind1])

    #plt.figure(figsize=(30,30))
    #plt.axis('off')
    #plt.imshow(labelled1)
    labelled1.save("groundtruth.tif")


    # In[15]:


    ind2 = np.random.choice(range(c_img.shape[0]))
    labelled2 = aug.draw_predict(c_img[ind2],lines)

    #plt.figure(figsize=(30,30))
    #plt.axis('off')
    #plt.imshow(labelled2)
    labelled2.save("predict.tif")


    # In[16]:


    blend_img = Image.blend(labelled1, labelled2, 0.3)
    #plt.figure(figsize=(30,30))
    #plt.axis('off')
    #plt.imshow(blend_img)
    blend_img.save("blend.tif")

