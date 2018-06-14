import json
import rectangle as rect
import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image, ImageDraw

class Dataset():
    def __init__(self):
        None
        
    def load_json(self):
        print('loading geojson into memory...')
        with open('xView_train.geojson') as f:
            data = json.load(f)
        
        coords = np.zeros((len(data['features']),4))
        chips = np.zeros((len(data['features'])),dtype="object")
        classes = np.zeros((len(data['features'])))
        
        for i in range(len(data['features'])):
            if data['features'][i]['properties']['bounds_imcoords'] != []:
                b_id = data['features'][i]['properties']['image_id']
                val = np.array([int(num) for num in data['features'][i]['properties']['bounds_imcoords'].split(",")])
                chips[i] = b_id
                classes[i] = data['features'][i]['properties']['type_id']
                if val.shape[0] != 4:
                    print("Issues at %d!" % i)
                else:
                    coords[i] = val
            else:
                chips[i] = 'None'
        self.coords = coords
        self.chips=chips
        self.classes=classes
        
        print('loading finished!')
        
    def load_txt(self,chip_name="5.tif"):
        print('loading training result into memory...')
        coords,areas,chips,classes,confs = [],[],[],[],[]
        f = open("predictions.txt")
        lines = f.readlines()
        for i in range(len(lines)):
            lines[i]=lines[i].split()
            xmin = int(lines[i][0])
            ymin = int(lines[i][1])
            xmax = int(lines[i][2])
            ymax = int(lines[i][3])
            cls  = int(lines[i][4])
            conf = float(lines[i][5])
            coords.append([xmin,ymin,xmax,ymax])
            areas.append((xmax-xmin)*(ymax-ymin))
            confs.append(conf)
            classes.append(cls)
            chips.append(chip_name)
            
        self.coords=np.array(coords)
        self.areas=np.array(areas)
        self.confs=np.array(confs)
        self.classes=np.array(classes)
        self.chips=np.array(chips)
        self.stat(chip_name)
        self.stat_data= self.stat(chip_name)
        print('loading finished!')
            
    def get_image(self,chip_name=None):
        if chip_name==None:
            chip_name=self.chips[0]
            
        self.image=np.array(Image.open(chip_name))
        
    def stat(self,chip_name=None,confidence=0):
        if chip_name==None:
            chip_name=self.chips[0]
        C=self.classes[np.logical_and(self.chips==chip_name, self.confs>=confidence)]
        A=self.areas[np.logical_and(self.chips==chip_name, self.confs>=confidence)]
        stat_data=[]
        x=0
        for i in np.unique(C):
            stat_data.append([])
            stat_data[x].append(i)
            
            stat_data[x].append(C.tolist().count(i))
            classArea=[]
            for j in range(len(C)):
                if i == C[j]:
                    classArea.append(A[j])
            stat_data[x].append(max(classArea))
            stat_data[x].append(min(classArea))
            stat_data[x].append(round(sum(classArea) / float(len(classArea)),2))
            x=x+1
        return stat_data

    def plot_bar(self,chip_name=None):
        if chip_name==None:
            chip_name=self.chips[0]
        
        Conf=self.confs[self.chips==chip_name]
        A=self.areas[self.chips==chip_name]
        self.stat(chip_name)
        yi=[]
        for i in self.stat_data:
            yi.append(i[1])
        x = np.linspace(0, len(yi)-1, len(yi))
        plt.xticks([])
        plt.xlabel("type")
        plt.ylabel("sample log10")
        plt.bar(x,np.log10(yi))
        if os.path.isfile("class.png"):
            os.system("erase "+"class.png")
        plt.savefig("class.png")
        plt.close()
        
        plt.xlabel("area")
        plt.ylabel("sample")
        plt.hist(A,8)
        if os.path.isfile("area.png"):
            os.system("erase "+"area.png")
        plt.savefig("area.png")
        plt.close()
        
        plt.xlabel("confidence")
        plt.ylabel("sample")
        plt.hist(Conf,10)
        if os.path.isfile("confidence.png"):
            os.system("erase "+"confidence.png")
        plt.savefig("confidence.png")
        plt.close()
        
    def draw_groundtruth(img,boxes):
        source = Image.fromarray(img)
        rects = Image.fromarray(img)
        draw = ImageDraw.Draw(rects)

        for i in range(boxes.shape[0]):
            xmin,ymin,xmax,ymax = boxes[i]
            for j in range(3):
                draw.rectangle(((xmin+j, ymin+j), (xmax+j, ymax+j)), fill=(240,10,10,1), outline='black')
                
        return Image.blend(rects, source, 0.4)

    def draw_predict(img,boxes,confs,confidence):

        source = Image.fromarray(img)
        rects = Image.fromarray(img)
        draw = ImageDraw.Draw(rects)

        for i in range(boxes.shape[0]):
            if confs[i] >= confidence:
                xmin,ymin,xmax,ymax = boxes[i]
                for j in range(3):
                    draw.rectangle(((xmin+j, ymin+j), (xmax+j, ymax+j)), fill=(10,240,10,1), outline='black')

        return Image.blend(rects, source, 0.4)

    def show_coords(self,chip_name,tag_classes,mode,confidence=None):
        if tag_classes == []:
            tag_classes=np.unique(self.classes)
        self.get_image(chip_name)
        #image list轉array需要強制改成unsigned int
        img = self.image
        img_coords = self.coords[self.chips==chip_name]
        img_classes = self.classes[self.chips==chip_name].astype(np.int64)
        if confidence != None:
            img_confs = self.confs[self.chips==chip_name]
        #產生T/F array
        X=[(img_classes==i) for i in tag_classes]
        truefalse=X[0]
        for i in X:
            truefalse=np.logical_or(truefalse,i)
        """
        truefalse = np.zeros(img_classes.shape[0], dtype=bool)
        for i in tag_classes:
            for j in range(len(img_classes)):
                if img_classes[j] == i:
                    truefalse[j] = True
        """
        img_coords = img_coords[truefalse]
        img_classes = img_classes[truefalse].astype(np.int64)
        if confidence != None:
            img_confs = img_confs[truefalse]

        if mode == 1:
            return Dataset.draw_groundtruth(img,img_coords)
        
        if mode == 2 and confidence!=None:
            return Dataset.draw_predict(img,img_coords,img_confs,confidence)


