#======================  
# imports  
#======================  
import tkinter as tk  
from tkinter import ttk  
from tkinter import scrolledtext  
from tkinter import Menu  
from tkinter import Spinbox  
from tkinter import messagebox as mBox
from tkinter.ttk import Style,Treeview 
from tkinter import filedialog
import aug_util as aug
import wv_util as wv
import rectangle as rect
import matplotlib.pyplot as plt
import numpy as np
import csv
import Dataset
import time
from PIL import ImageTk, Image  
  
#由于tkinter中没有ToolTip功能，所以自定义这个功能如下  
class ToolTip(object):  
    def __init__(self, widget):  
        self.widget = widget  
        self.tipwindow = None  
        self.id = None  
        self.x = self.y = 0  
  
    def showtip(self, text):  
        "Display text in tooltip window"  
        self.text = text  
        if self.tipwindow or not self.text:  
            return  
        x, y, _cx, cy = self.widget.bbox("insert")  
        x = x + self.widget.winfo_rootx() + 27  
        y = y + cy + self.widget.winfo_rooty() +27  
        self.tipwindow = tw = tk.Toplevel(self.widget)  
        tw.wm_overrideredirect(1)  
        tw.wm_geometry("+%d+%d" % (x, y))  
  
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,  
                      background="#ffffe0", relief=tk.SOLID, borderwidth=1,  
                      font=("tahoma", "8", "normal"))  
        label.pack(ipadx=1)  
  
    def hidetip(self):  
        tw = self.tipwindow  
        self.tipwindow = None  
        if tw:  
            tw.destroy()  
              
#===================================================================            
def createToolTip( widget, text):  
    toolTip = ToolTip(widget)  
    def enter(event):  
        toolTip.showtip(text)  
    def leave(event):  
        toolTip.hidetip()  
    widget.bind('<Enter>', enter)  
    widget.bind('<Leave>', leave)  
groundtruth=Dataset.Dataset()
training_result=Dataset.Dataset()  
# Create instance  
win = tk.Tk()     
  
# Add a title         
win.title("xView")  
  
# Disable resizing the GUI  
win.resizable(0,0)  
  
# Tab Control introduced here --------------------------------------  
"""tabControl = ttk.Notebook(win)          # Create Tab Control  
  
tab1 = ttk.Frame(tabControl)            # Create a tab   
tabControl.add(tab1, text='第一頁')      # Add the tab  
  
tab2 = ttk.Frame(tabControl)            # Add a second tab  
tabControl.add(tab2, text='第二頁')      # Make second tab visible  
  
tab3 = ttk.Frame(tabControl)            # Add a third tab  
tabControl.add(tab3, text='第三頁')      # Make second tab visible  
  
tabControl.pack(expand=1, fill="both")  # Pack to make visible"""  
# ~ Tab Control introduced here -----------------------------------------  
  
#---------------Tab1控件介绍------------------#  
# We are creating a container tab3 to hold all other widgets  

s = Style()
btnimg1=ImageTk.PhotoImage(Image.open("GTbutton.png"))
s.configure('GT.TButton', padding=6, relief="flat",image=btnimg1)
btnimg2=ImageTk.PhotoImage(Image.open("Rbutton.png"))
s.configure('R.TButton', padding=6, relief="flat",image=btnimg2)
btnimg3=ImageTk.PhotoImage(Image.open("GTbutton_press.png"))
s.configure('GT_press.TButton', padding=6, relief="flat",image=btnimg3)
btnimg4=ImageTk.PhotoImage(Image.open("Rbutton_press.png"))
s.configure('R_press.TButton', padding=6, relief="flat",image=btnimg4)





root = ttk.Frame()  
root.grid(column=10, row=10, padx=8, pady=4)  

filename = "5.tif"
filepath = "5.tif"
 
GTflag=0
Rflag=0 
selected=[]
# Modified Button Click Function  
def clickGT():
    global GTflag
    if GTflag==0:
        GTflag=1
        buttonGT.configure(style='GT_press.TButton')
        
    else:
        GTflag=0
        buttonGT.configure(style='GT.TButton')
    
    change() 
    #action1.configure(text='Hello\n ' + confidence.get())  
    #action1.configure(state='disabled')    # Disable the Button Widget  
def clickR():
    global Rflag
    if Rflag==0:
        Rflag=1
        buttonR.configure(style='R_press.TButton')
    else:
        Rflag=0
        buttonR.configure(style='R.TButton')
    change()
    #action1.configure(text='Hello\n ' + confidence.get())  
    #action1.configure(state='disabled')    # Disable the Button Widget
def change():
    
    if GTflag==1 and Rflag==1:
        imgGT=groundtruth.show_coords(filename,selected,1)
        imgR=training_result.show_coords(filename,selected,2,float(confidence.get()))
        img=Image.blend(imgGT,imgR,0.3)
    elif GTflag==1 and Rflag==0:
        img=groundtruth.show_coords(filename,selected,1)
    elif GTflag==0 and Rflag==1:
        img=training_result.show_coords(filename,selected,2,float(confidence.get()))
    else:
        img = Image.open(filepath)
    img_output = ImageTk.PhotoImage(img.resize((650,650),Image.ANTIALIAS))
    imgLabel.configure(image=img_output)
    imgLabel.image = img_output

#圖名
fileNameLabel=ttk.Label(root)
fileNameLabel.grid(column=0, row=0,columnspan=2,sticky='W')
#信心  
ttk.Label(root, text="confidence :").grid(column=2, row=0,sticky='W')
confidence = tk.StringVar()
confidence.set('0')  
confidenceEntry = ttk.Entry(root, width=6, textvariable=confidence)  
confidenceEntry.grid(column=3, row=0, sticky='W')
def confidenceEnter(event):
    tree.delete(*tree.get_children())
    count=training_result.stat(filename,float(confidence.get()))
    for i in range(len(count)):
        tree.insert('', i, values=[str(count[i][0]),str(count[i][1]),str(count[i][2]),str(count[i][3]),str(count[i][4])])
    change()
confidenceEntry.bind('<Return>',confidenceEnter)  
#圖片


imgLabel=ttk.Label(root)
imgLabel.grid(column=0, row=1,columnspan=4,rowspan=2, sticky='W')
#按鈕


buttonGT = ttk.Button(root,command=clickGT,style='GT.TButton')     
buttonGT.grid(column=4,row=0)  
buttonR = ttk.Button(root,command=clickR,style='R.TButton')     
buttonR.grid(column=5,row=0)  
#buttonIntersection = ttk.Button(root,text="Intersection",command=clickMe)     
#buttonIntersection.grid(column=6,row=0)
# Using a scrolled Text control      
scrolW  = 75; scrolH  =  20  
scr = scrolledtext.ScrolledText(root, wrap=tk.WORD,width=scrolW,height=scrolH)  
scr.grid(column=4, row=1, sticky='WN', columnspan=2)
#直方圖
tabControl = ttk.Notebook(root)          # Create Tab Control  
  
tab1 = ttk.Frame(tabControl)            # Create a tab   
tabControl.add(tab1, text='類別數量分佈圖')      # Add the tab  
  
tab2 = ttk.Frame(tabControl)            # Add a second tab  
tabControl.add(tab2, text='面積大小分佈圖')      # Make second tab visible  
  
tab3 = ttk.Frame(tabControl)            # Add a third tab  
tabControl.add(tab3, text='信心分佈圖')      # Make second tab visible  
 
tabControl.grid(column=4,row=2,columnspan=2,sticky='NWES')  # Pack to make visible
hist1=ttk.Label(tab1)
hist1.grid(column=0,row=0,sticky='NWES')  
hist2=ttk.Label(tab2)
hist2.grid(column=0,row=0,sticky='NWES')  
hist3=ttk.Label(tab3)
hist3.grid(column=0,row=0,sticky='NWES')    

#滚动条

scrollBar = tk.Scrollbar(root)

scrollBar.grid(column=6,row=1,rowspan=2,sticky='E')

#Treeview组件，6列，显示表头，带垂直滚动条

tree = Treeview(root,

                          columns=('c1', 'c2', 'c3',

                                           'c4', 'c5'),

                          show="headings",

                          yscrollcommand=scrollBar.set)

#设置每列宽度和对齐方式

tree.column('c1', width=40, anchor='center')

tree.column('c2', width=50, anchor='center')

tree.column('c3', width=60, anchor='center')

tree.column('c4', width=60, anchor='center')

tree.column('c5', width=150, anchor='center')


#设置每列表头标题文本

tree.heading('c1', text='Type')

tree.heading('c2', text='sample')

tree.heading('c3', text='Max')

tree.heading('c4', text='Min')

tree.heading('c5', text='Average')


tree.grid(column=6,row=1,rowspan=2,sticky='NSEW')

#Treeview组件与垂直滚动条结合

scrollBar.config(command=tree.yview)

#定义并绑定Treeview组件的鼠标单击事件

def treeviewClick(event):
    for item in tree.selection():
        item_tag = tree.item(item,"tags")
        item_value = tree.item(item,"values")
        tree.item(item,tags=1)
        print(item_value)
        print(item_tag)

tree.bind('<ButtonRelease-1>', treeviewClick)

"""
# Adding a Combobox  
book = tk.StringVar()  
bookChosen = ttk.Combobox(root, width=12, textvariable=book)  
bookChosen['values'] = ('平凡的世界', '亲爱的安德烈','看见','白夜行')  
bookChosen.grid(column=1, row=1)  
bookChosen.current(0)  #设置初始显示值，值为元组['values']的下标  
bookChosen.config(state='readonly')  #设为只读模式  
  
# Spinbox callback   
def _spin():  
    value = spin.get()  
    #print(value)  
    scr.insert(tk.INSERT, value + '\n')  
  
def _spin2():  
    value = spin2.get()  
    #print(value)  
    scr.insert(tk.INSERT, value + '\n')  
       
# Adding 2 Spinbox widget using a set of values  
spin = Spinbox(root, from_=10,to=25, width=5, bd=8, command=_spin)   
spin.grid(column=0, row=2)  
  
spin2 = Spinbox(root, values=('Python3入门', 'C语言','C++', 'Java', 'OpenCV'), width=13, bd=3, command=_spin2)   
spin2.grid(column=1, row=2,sticky='W')  
"""   

  
# Add Tooltip  
#createToolTip(spin,       '这是一个Spinbox.')  
#createToolTip(spin2,      '这是一个Spinbox.')  
createToolTip(buttonGT,     '紅色部分.')
createToolTip(buttonR,'綠色部分')  
createToolTip(confidenceEntry,'輸入0到1.')  
#createToolTip(bookChosen, '这是一个Combobox.')  
createToolTip(scr,        '这是一个ScrolledText.')  
  
# 一次性控制各控件之间的距离  
for child in root.winfo_children():   
    child.grid_configure(padx=3,pady=1)  
# 单独控制个别控件之间的距离  
#action.grid(column=2,row=1,rowspan=2,padx=6)  
#---------------Tab1控件介绍------------------#  
  
""" 
#---------------Tab2控件介绍------------------#  
# We are creating a container tab3 to hold all other widgets -- Tab2  
monty2 = ttk.LabelFrame(tab2, text='控件示范区2')  
monty2.grid(column=0, row=0, padx=8, pady=4)  
# Creating three checkbuttons  
chVarDis = tk.IntVar()  
check1 = tk.Checkbutton(monty2, text="失效选项", variable=chVarDis, state='disabled')  
check1.select()    
check1.grid(column=0, row=0, sticky=tk.W)                   
  
chVarUn = tk.IntVar()  
check2 = tk.Checkbutton(monty2, text="遵从内心", variable=chVarUn)  
check2.deselect()   #Clears (turns off) the checkbutton.  
check2.grid(column=1, row=0, sticky=tk.W )                    
   
chVarEn = tk.IntVar()  
check3 = tk.Checkbutton(monty2, text="屈于现实", variable=chVarEn)  
check3.deselect()  
check3.grid(column=2, row=0, sticky=tk.W)                   
  
# GUI Callback function   
def checkCallback(*ignoredArgs):  
    # only enable one checkbutton  
    if chVarUn.get(): check3.configure(state='disabled')  
    else:             check3.configure(state='normal')  
    if chVarEn.get(): check2.configure(state='disabled')  
    else:             check2.configure(state='normal')   
   
# trace the state of the two checkbuttons  #？？  
chVarUn.trace('w', lambda unused0, unused1, unused2 : checkCallback())      
chVarEn.trace('w', lambda unused0, unused1, unused2 : checkCallback())     
  
# Radiobutton list  
values = ["富强民主", "文明和谐", "自由平等","公正法治","爱国敬业","诚信友善"]  
  
# Radiobutton callback function  
def radCall():  
    radSel=radVar.get()  
    if   radSel == 0: monty2.configure(text='富强民主')  
    elif radSel == 1: monty2.configure(text='文明和谐')  
    elif radSel == 2: monty2.configure(text='自由平等')  
    elif radSel == 3: monty2.configure(text='公正法治')  
    elif radSel == 4: monty2.configure(text='爱国敬业')  
    elif radSel == 5: monty2.configure(text='诚信友善')  
  
# create three Radiobuttons using one variable  
radVar = tk.IntVar()  
  
# Selecting a non-existing index value for radVar  
radVar.set(99)      
  
# Creating all three Radiobutton widgets within one loop  
for col in range(4):  
    #curRad = 'rad' + str(col)    
    curRad = tk.Radiobutton(monty2, text=values[col], variable=radVar, value=col, command=radCall)  
    curRad.grid(column=col, row=6, sticky=tk.W, columnspan=3)  
for col in range(4,6):  
    #curRad = 'rad' + str(col)    
    curRad = tk.Radiobutton(monty2, text=values[col], variable=radVar, value=col, command=radCall)  
    curRad.grid(column=col-4, row=7, sticky=tk.W, columnspan=3)  
  
style = ttk.Style()  
style.configure("BW.TLabel", font=("Times", "10",'bold'))  
ttk.Label(monty2, text="   社会主义核心价值观",style="BW.TLabel").grid(column=2, row=7,columnspan=2, sticky=tk.EW)  
  
# Create a container to hold labels  
labelsFrame = ttk.LabelFrame(monty2, text=' 嵌套区域 ')  
labelsFrame.grid(column=0, row=8,columnspan=4)  
   
# Place labels into the container element - vertically  
ttk.Label(labelsFrame, text="你才25岁，你可以成为任何你想成为的人。").grid(column=0, row=0)  
ttk.Label(labelsFrame, text="不要在乎一城一池的得失，要执着。").grid(column=0, row=1,sticky=tk.W)  
  
# Add some space around each label  
for child in labelsFrame.winfo_children():   
    child.grid_configure(padx=8,pady=4)  
#---------------Tab2控件介绍------------------#  
  
  
#---------------Tab3控件介绍------------------#  
tab3 = tk.Frame(tab3, bg='#AFEEEE')  
tab3.pack()  
for i in range(2):  
    canvas = 'canvas' + str(col)  
    canvas = tk.Canvas(tab3, width=162, height=95, highlightthickness=0, bg='#FFFF00')  
    canvas.grid(row=i, column=i)  
#---------------Tab3控件介绍------------------#  
  
"""  
#----------------菜单栏介绍-------------------#      
# Exit GUI cleanly  
def _quit():  
    win.quit()  
    win.destroy()  
    exit()  
def _open():
    global filepath
    img = ImageTk.PhotoImage(Image.open(filepath).resize((650,650),Image.ANTIALIAS))
    imgLabel.configure(image=img)
    imgLabel.image = img
    fileNameLabel.configure(text="檔案名稱 : " + filename)
    #print(filename)
    groundtruth.load_json()
    training_result.load_txt(filename)
    training_result.plot_bar(filename)
    
    h1 = ImageTk.PhotoImage(Image.open("class.png").resize((525,350),Image.ANTIALIAS))
    h2 = ImageTk.PhotoImage(Image.open("area.png").resize((525,350),Image.ANTIALIAS))
    h3 = ImageTk.PhotoImage(Image.open("confidence.png").resize((525,350),Image.ANTIALIAS))
    hist1.configure(image=h1)
    hist2.configure(image=h2)
    hist3.configure(image=h3)
    hist1.image = h1
    hist2.image = h2
    hist3.image = h3
    
    count=training_result.stat_data
    for i in range(len(count)):
        tree.insert('', i, values=[str(count[i][0]),str(count[i][1]),str(count[i][2]),str(count[i][3]),str(count[i][4])],tags=0)
    
"""
    dlg = win32ui.CreateFileDialog(1) # 1表示打开文件对话框
    dlg.SetOFNInitialDir('E:/Python') # 设置打开文件对话框中的初始显示目录
    dlg.DoModal()
 
    filename = dlg.GetPathName() # 获取选择的文件名称
    print (filename)
"""  
# Creating a Menu Bar  
menuBar = Menu(win)  
win.config(menu=menuBar)  
  
# Add menu items  
fileMenu = Menu(menuBar, tearoff=0)  
fileMenu.add_command(label="Open",command=_open)  
fileMenu.add_separator()  
fileMenu.add_command(label="Exit", command=_quit)  
menuBar.add_cascade(label="File", menu=fileMenu)  
  
"""  
# Display a Message Box  
def _msgBox1():  
    mBox.showinfo('Python Message Info Box', '通知：程序运行正常！')  
def _msgBox2():  
    mBox.showwarning('Python Message Warning Box', '警告：程序出现错误，请检查！')  
def _msgBox3():  
    mBox.showwarning('Python Message Error Box', '错误：程序出现严重错误，请退出！')  
def _msgBox4():  
    answer = mBox.askyesno("Python Message Dual Choice Box", "你喜欢这篇文章吗？\n您的选择是：")   
    if answer == True:  
        mBox.showinfo('显示选择结果', '您选择了“是”，谢谢参与！')  
    else:  
        mBox.showinfo('显示选择结果', '您选择了“否”，谢谢参与！')  
  
# Add another Menu to the Menu Bar and an item  

msgMenu = Menu(menuBar, tearoff=0)  
msgMenu.add_command(label="通知 Box", command=_msgBox1)  
msgMenu.add_command(label="警告 Box", command=_msgBox2)  
msgMenu.add_command(label="错误 Box", command=_msgBox3)  
msgMenu.add_separator()  
msgMenu.add_command(label="判断对话框", command=_msgBox4)  
menuBar.add_cascade(label="Info", menu=msgMenu)  
"""
#----------------菜单栏介绍-------------------#  
  
  

  
# Place cursor into name Entry  
confidenceEntry.focus()        
#======================  
# Start GUI  
#======================  
win.mainloop()  