import os
import yagmail
import cv2
import torch
from matplotlib import pyplot as plt
import numpy as np
from unicodedata import name
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import sys
from PyQt5 import QtWidgets,QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMainWindow
from PyQt5.uic import loadUi
from cv2 import readOpticalFlow
import matplotlib
from tensorflow.python.framework.ops import RegisterStatistics
import shutil
#selectedvideo=""
model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5/runs/train/exp/weights/best (2).pt')#, force_reload=True)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi("home.ui",self)
        self.Browse.clicked.connect(self.browsefiles)
        self.Browse_2.clicked.connect(self.connectedcam)
        self.Browse_3.clicked.connect(self.respodents)
        self.Browse_4.clicked.connect(self.respodentsoverwrite)
        self.algorithm.clicked.connect(self.algorithmr)
        self.path=None

    def browsefiles(self):
        fname=QFileDialog.getOpenFileName(self, 'open file')
        vid =cv2.VideoCapture(fname[0])
        global selectedvideo 
        selectedvideo= fname[0]
        # frame
        currentframe = 0
        while(currentframe<1):
                  
                # reading from frame
                ret,frame = vid.read()

                if ret:
                        # if video is still left continue creating images
                        name = 'thumbnail.jpg'
                        print ('Creating...' + name)
          
                        # writing the extracted images
                        cv2.imwrite(name, frame)
          
                        # increasing counter so that it will
                        # show how many frames are created
                        currentframe += 1
                else:
                        break
        # Release all space and windows once done
        vid.release()
        cv2.destroyAllWindows()               
        self.sphoto.setPixmap(QtGui.QPixmap('thumbnail.jpg'))
        print(selectedvideo)
        #return  selectedvideo  
           
    def respodents(self):
        with open('respodents.txt','a') as respodents:
                #respodents.seek(0)
                respodents.write(str(self.textEdit.toPlainText())+",")
                #myfile.truncate()
        self.textEdit.setText("ADDED!")

    def respodentsoverwrite(self):
        with open('respodents.txt','w') as respodents:
                #respodents.seek(0)
                respodents.write(str(self.textEdit.toPlainText())+",")
                #myfile.truncate()
        self.textEdit.setText("ADDED! through Overwrite")
        
    def connectedcam(self):
        #fname=QFileDialog.getOpenFileName(self, 'open file')
        vid =cv2.VideoCapture(0)
        global selectedvideo 
        selectedvideo= 0
        # frame
        currentframe = 0
        while(currentframe<1):
                  
                # reading from frame
                ret,frame = vid.read()

                if ret:
                        # if video is still left continue creating images
                        name = 'thumbnail.jpg'
                        print ('Creating...' + name)
          
                        # writing the extracted images
                        cv2.imwrite(name, frame)
          
                        # increasing counter so that it will
                        # show how many frames are created
                        currentframe += 1
                else:
                        break
        # Release all space and windows once done
        vid.release()
        cv2.destroyAllWindows()               
        self.sphoto.setPixmap(QtGui.QPixmap('thumbnail.jpg'))
        print(selectedvideo)
        #return  selectedvideo             
    def algorithmr(self):
        print(selectedvideo)
        frespodents=[]
        with open('respodents.txt','r+') as respodents:
                data = respodents.read()
                demails=[data+"end"]
                stringe = demails[0]
                emails = stringe.split(',')
                print(emails)
        for k in range(0,(len(emails)-1)):
                frespodents.append(emails[k])
        print(frespodents)
        cap = cv2.VideoCapture(selectedvideo)
        firesizehistory=[]
        firesizehistory.append(0)
        fireareaperframe=[]
        font = cv2.FONT_HERSHEY_SIMPLEX
        unit=1
        framecounter=0
        while cap.isOpened():
                ret, frame = cap.read()
                if ret:
                        if framecounter % 5 == 0:
                                # Make detections 
                                results = model(frame)
                                results
                                results.xyxy
                                rectangle_size = frame.shape[0]*frame.shape[1]
                                rectangle_size
                                sumfs=0
                                firesz = [] 
                                for idx in range(0,len(results.xyxy[0])):
                                        length = np.subtract(results.xyxy[0][idx][2], results.xyxy[0][idx][0])
                                        height = np.subtract(results.xyxy[0][idx][3], results.xyxy[0][idx][1])
                                        
                                        firearea=length*height
                                        firesz.append(firearea)
                                for i in range(0, len(firesz)):    
                                        sumfs = sumfs + firesz[i]; 
                                sumfs
                                rectangle_size
                                if sumfs > 0:
                                        fireareaperframe.append(int(sumfs))
                                        if len(fireareaperframe) == 1:
                                                cv2.imwrite("detected.jpg", np.squeeze(results.render()))
                                                yag = yagmail.SMTP(user='@gmail.com', password='')
                                                #sending the email
                                                
                                                yag.send(to=frespodents, subject='Fire alert', contents='Fire detected!!!!', attachments=['detected.jpg'])
                                                print("Email sent successfully")
                                        firesizepercentage=sumfs/rectangle_size*100
                                        int(firesizepercentage)
                                        firesizehistory.append(int(firesizepercentage))
                                        
                                        if (firesizehistory[unit])>= firesizehistory[(unit)-1]:
                                                cv2.putText(frame, 
                                                        'fire is increasing', 
                                                        (50, 50), 
                                                        font, 1, 
                                                        (0, 255, 255), 
                                                        2, 
                                                        cv2.LINE_4)
                                        elif (firesizehistory[unit])< firesizehistory[(unit)-1]:
                                                        cv2.putText(frame, 
                                                        'fire is decreasing', 
                                                        (50, 50), 
                                                        font, 1, 
                                                        (0, 255, 255), 
                                                        2, 
                                                        cv2.LINE_4)
                                        
                                        unit=unit+1
                                cv2.imshow('YOLO', np.squeeze(results.render()))
                        framecounter=framecounter+1
                else:
                        break      
                if cv2.waitKey(10) & 0xFF == ord('q'):
                        break
        cap.release()
        cv2.destroyAllWindows()
        #Draws a graph for the results
        fig, axes = plt.subplots(1,2, figsize=(16,7))
        axes[0].set_title('firesizehistory' , c='r' , fontsize=15)
        axes[0].plot(firesizehistory, color='blue', label='train loss')
        axes[1].set_title('firesizearea' , c='r' , fontsize=15)
        axes[1].plot(fireareaperframe, color='blue', label='train loss')
        plt.savefig("model1.png")
        #%matplotlib inline
        # results graph
        plt.subplot(211)
        plt.title('fizesize')
        plt.plot(firesizehistory, label='fizesize')
        plt.legend()
        plt.savefig("model2.png")
        #importing the Yagmail library
        #import yagmail

        try:
                #initializing the server connection
                yag = yagmail.SMTP(user'@gmail.com', password='')
                #sending the email
                yag.send(to=frespodents, subject='Fire alert', contents='Fire detected!!!!', attachments=['model1.png','detected.jpg'])
                print("Email sent successfully")
        except:
                print("Error, email was not sent")
        if len(firesizehistory)>0:
                max_value = np.max(firesizehistory)
        else:
                max_value=0
        
        with open('myfile.txt','r+') as myfile:
                myfile.seek(0)
                myfile.write(str(max_value)+"%")
                myfile.truncate()
        os.system('summary.py') 


app=QApplication(sys.argv)
mainwindow=MainWindow()
Widget=QtWidgets.QStackedWidget()
Widget.addWidget(mainwindow)
Widget.setFixedWidth(951)
Widget.setFixedHeight(781)
Widget.show()
sys.exit(app.exec_())



