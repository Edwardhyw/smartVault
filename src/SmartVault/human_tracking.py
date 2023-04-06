import cv2
import mediapipe as mp
import time
import serial
import save_image
from diff import *

class human_tracking:
    def __init__(self, port = None, baudrate = None, servo = None):
        self.port = port #serial port on laptop
        self.baudrate = baudrate #serial communication baudrate
        self.servo = servo #use servo or not
        if self.port is None and self.baudrate is None:
            self.ser = None
        else:
            self.ser = serial.Serial(port, baudrate)
        time.sleep(2)
        self.mpPose = mp.solutions.pose #initialize the pose tracking module
        self.mpDraw = mp.solutions.drawing_utils
        self.pose = self.mpPose.Pose()
        self.cap = cv2.VideoCapture(1+cv2.CAP_DSHOW)
        self.old_state = 0
        self.new_state = 0
        self.image1 = None
        self.image2 = None
        self.flag = 0
        self.pTime = 0
        self.cTime = 0


    def newfun(self):
        while True:
            begin_tracking

    def begin_tracking(self,path):
        success, img = self.cap.read()
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        result = self.pose.process(imgRGB)
        self.old_state = self.new_state

        if result.pose_landmarks: #This is when human detect, new state become 1
            self.new_state = 1 
            self.mpDraw.draw_landmarks(img,result.pose_landmarks,self.mpPose.POSE_CONNECTIONS) # draw the landmark on image
            xavg = 0
            yavg = 0
            counter = 0
            for id,lm in enumerate(result.pose_landmarks.landmark): # This for loop is to count how many joints are in the image, in order to calculate the mass center
                h,w,c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                if lm.visibility>0.9:
                    xavg = xavg + int(lm.x*w) 
                    yavg = yavg + int(lm.y*h) 
                    counter = counter +1
            if counter != 0:
                xavg = xavg/counter #xavg is the x coordinate of mass center
                yavg = yavg/counter #yavg is the y coordinate of mass center
            else :
                xavg = 0
                yavg = 0
            cv2.circle(img, (int(xavg), int(yavg)), 10, (255, 0, 0), cv2.FILLED)
            h, w, c = img.shape
            xcenter = w/2;
            ycenter = h/2;
            
            #--------------------------------------------------------------------------------------------------
            '''If the serial port is connected, it will start the detection. When the mass center of human move out
            of the boundary, it will send a signal to Arduino'''
            if self.port:
                if xavg > xcenter+50:
                    self.ser.write('d'.encode('utf-8'))
                    #print('sent d')

                if xavg < xcenter - 50:
                    self.ser.write('i'.encode('utf-8'))
                    #print('sent i')

                if yavg > ycenter + 50:
                    self.ser.write('3'.encode('utf-8'))
                    #print('sent 3')

                if yavg < ycenter - 50:
                    self.ser.write('4'.encode('utf-8'))
                    #print('sent 4')
        else:
            self.new_state = 0

        #if self.new_state - self.old_state == 0:
            #print("no change")
            #-------------------------------------------------------------------------------------
            '''Here we start detecting if the hunman come into the room or out of the room, or stay in the room'''
        if self.new_state == 1:
            self.pTime = 0

        if self.new_state - self.old_state == 1:
            print("human coming")

        if self.new_state - self.old_state == -1:
            print("human leaving")
            
            if self.port == None:
                self.flag = 1
            self.pTime = time.time() #record the time when human leave the room

        self.cTime = time.time() # record the current time
        
        '''Send back to origin command to arduino after human leave 3 sec, then send signal to Arduino to make camera rotate
        back to the original angle. Then the camera will stay for 8 sec, then take a photo of the room'''
        if (self.cTime - self.pTime) > 3 and self.pTime != 0 and self.port: 
            print("back to origin")
            self.ser.write('o'.encode('utf-8'))
            time.sleep(8)
            success, img = self.cap.read()
            self.image1 = self.image2
            self.image2 = self.cap.read()[1]
            if self.flag > 0:
                extract_item(path, self.image1, self.image2)
                cv2.imwrite(path+'image1.jpg',self.image1)
                cv2.imwrite(path+'image2.jpg',self.image2)
            self.flag = self.flag +1
            print(self.flag)
            self.pTime = 0
            print('servo extracted')
            print('image1')
            #print(self.image1)
            print('image2')
            #print(self.image2)


        cv2.imshow("image",img) # Show image to users
        cv2.waitKey(1)



    def Move_to_Origin(self): #This is the funcion to send signal to Arduino make camera back to orgin
        self.ser.write('o'.encode('utf-8'))
        print("back to origin")
        time.sleep(5)

    #def return_img(self):
        # return the image


