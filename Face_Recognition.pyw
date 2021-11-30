import sys
from tkinter import *
import tkinter as tk
import os
import time
import tkinter

try:
    import shutil
except:
    os.system("pip install pytest-shutil")
try:
    import cv2
except:
    os.system("pip install opencv-python")
try:
    import win32com.client
except:
    os.system("pip install pywin32")
try:
    import numpy as np
except:
    os.system("pip install numpy")
try:
    from PIL import Image
except:
    os.system("pip install Pillow")


Voice = win32com.client.Dispatch("SAPI.SpVoice")
def speak(data):
    Voice.Speak(data)
    
speak("Welcome To our face recognition software,created by Ajay Sundaran")

try:
    os.remove("./Faces/Demo.txt")
except:
    pass
root = Tk()
root.wait_visibility(root)
#root.call('wm', 'attributes', '.', '-topmost', '1')
root.wm_attributes('-alpha',0.85)
root['background']='#336171'
root.title("21BAS10108 (Ajay Sundaran VIT Bhopal)")
root.resizable(0,0)
root.geometry("800x550")
bg = PhotoImage(file = "./Src/bg.jpg")
canvas1 = Canvas( root, width = 400,height = 400)
canvas1.pack(fill = "both", expand = True)
canvas1.create_image( 0, 0, image = bg,anchor = "nw")
canvas1.create_text( 200, 250, text = "Welcome")



reg_num = "21BAS10108"


traniner_location = "Src/trainer.yml"
dataset_location = "Src/haarcascade_frontalface_default.xml"



def gui_exit():
    root.destroy()
    speak("Thanks for using This software")
    sys.exit()

def reset():
    speak("Deleting Please Wait")
    f1 = open("./Src/Id.txt","w")
    f1.write("0")
    f1.close()
    
    f1 = open("./Src/Name.txt","w")
    f1.write("None")
    f1.close()
    try:
        dir = './Faces/'
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))
            
        os.remove("./Src/trainer.yml")
        speak("files deleted sucessfully")
    except:
        speak("I think files or already cleared")


def collect():        
        
    
    speak("please show your face in front of camera")
    cam = cv2.VideoCapture(1)
    cam.set(3, 640)
    cam.set(4, 480)    
    face_detector = cv2.CascadeClassifier(dataset_location)

    f2 = open("./Src/Id.txt","r")
    id_data  = f2.readlines()
    f2.close()
    

    try:
        data = id_data[-1:][0]
        data = (int(data))+1
        data_face = str(data)
        f3 = open("./Src/Id.txt","a")
        f3.write("\n"+data_face)
        f3.close()
        data_face = str(data)
    except Exception as e:
        
        f3 = open("./Src/Id.txt","w")
        f3.write("0\n1")
        f3.close()
        data_face = "1"
        
        
    
    face_id = data_face
    speak("Initializing face capture,please make sure that camera is connected")
    count = 0
    while(True):
        ret, img = cam.read()
        img = cv2.flip(img, -1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
            count += 1
            cv2.imwrite("Faces/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
            cv2.imshow(reg_num, img)
        k = cv2.waitKey(100) & 0xff
        if k == 27:
            break
        elif count >= 30:
             break
    speak("datas collected")
    cam.release()
    cv2.destroyAllWindows()
    trainer()

def trainer():
    speak("Training faces. It will take a few seconds. Wait ...")    
    path = 'Faces'
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier(dataset_location);

    def getImagesAndLabels(path):
        imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
        faceSamples=[]
        ids = []
        for imagePath in imagePaths:
            PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
            img_numpy = np.array(PIL_img,'uint8')
            id = int(os.path.split(imagePath)[-1].split(".")[1])
            faces = detector.detectMultiScale(img_numpy)
            for (x,y,w,h) in faces:
                faceSamples.append(img_numpy[y:y+h,x:x+w])
                ids.append(id)
        return faceSamples,ids
    
    faces,ids = getImagesAndLabels(path)
    recognizer.train(faces, np.array(ids))
    recognizer.write(traniner_location)
    speak(" {0} faces trained successfully".format(len(np.unique(ids))))


def recognize_main():
    speak("Show your face in front of camera")
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(traniner_location)
    cascadePath = dataset_location
    faceCascade = cv2.CascadeClassifier(cascadePath);    
    font = cv2.FONT_HERSHEY_SIMPLEX
    id = 0
    
    a_file = open("./Src/Name.txt", "r")
    lines = a_file.readlines()
    

    #########    
    names = lines
    #########

    
    cam = cv2.VideoCapture(1)
    cam.set(3, 640)
    cam.set(4, 480)
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)
    
    while True:
        ret, img =cam.read()
        img = cv2.flip(img, 0)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        
        faces = faceCascade.detectMultiScale( 
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
           )
    
        for(x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
            if (confidence < 100):
                #(confidence)
                id = names[id].replace("\n","")
                confidence = "  {0}%".format(round(100 - confidence))
            else:
                id = "unknown"
                confidence = "  {0}%".format(round(100 - confidence))
            
            cv2.putText(img, str(id), (x+5,y-5), font, 1, (0,0,0), 2)
            cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
        
        cv2.imshow(reg_num,img) 
    
        k = cv2.waitKey(10) & 0xff 
        if k == 27:
            break
    
    
    speak("Face Recognition Cancelled")
    cam.release()
    cv2.destroyAllWindows()

def recognize():
    try:
        recognize_main()
    except:
        speak("Error Found,I think there is no trained,face")

def new_window():
    def command_new():
        name = e1.get()
        speak("Please Wait")
        new.destroy()
        
        
        f0 = open("./Src/Name.txt","r")
        face_name  = f0.readlines()
        f0.close()
        
        try:
            face_name = face_name[-1:][0]
            name_face = str(face_name)
            f1 = open("./Src/Name.txt","a")
            f1.write("\n"+name)
            f1.close()
        except Exception as e:
            (e)
            f1 = open("./Src/Name.txt","w")
            f1.write("None\n"+name)
            f1.close()

        try:
            collect()
        except:
            speak("Sorry I am unable to recognize face")
        
    def new_exit():
        new.destroy()
    speak("Please Enter The Name of the Face")
    new = Tk()
    new.geometry("400x100")
    new.call('wm', 'attributes', '.', '-topmost', '1')
    new.wm_attributes('-alpha',0.85)
    new['background']='#336171'
    new.title("21BAS10108 (Ajay Sundaran VIT Bhopal)")
    new.resizable(0,0)
    tk.Label(new,foreground = '#00ffff',background= '#336171' ,text=" ").grid(row=1)
    tk.Label(new,foreground = '#00ffff',background= '#336171' ,text="Name of Face : ").grid(row=2)
    e1 = tk.Entry(new, bd =5, width=45, background= '#336171', foreground = '#00ffff')
    e1.grid(row=2, column=1)
    tk.Button(new, text='Conform Name',background= '#336171',foreground = '#00ffff' , command=command_new).grid(row=4, column=0, sticky=tk.W, pady=4)
    tk.Button(new, text='Quit',background= '#336171',foreground = '#00ffff' , command=new_exit).grid(row=4, column=1, sticky=tk.W, pady=4)

def gui_help():
    speak("Help!")
    help_data = """
        * To press 'Add Face' Button to build face dictionary
        * To press 'Recognize Face' Button to Recognize Face from face dictionary
        * To press 'Clear Face Data' Button to Clear Face Dictionary of users
        * To press 'Exit' Button to Exit Program
        * To press 'Esc' key to close recognize window
        """

    new1 = Tk()
    
    new1.geometry("700x250")
    new1.call('wm', 'attributes', '.', '-topmost', '1')
    new1.wm_attributes('-alpha',0.85)
    new1['background']='#336171'
    new1.title("21BAS10108 (Ajay Sundaran VIT Bhopal) - Help!")
    new1.resizable(0,0)
    T = Text(new1, height = 10, width = 85,foreground = "#00ffff", background="#336171")
    l = Label(new1, text = "Instructions",foreground = "#00ffff", background="#336171")
    l.config(font =("Courier", 14)) 
    b1 = Button(new1, text = "Exit",command = new1.destroy) 
    l.pack()
    T.pack()
    b1.pack()
    T.insert(tk.END, help_data)
    T.config(state=tkinter.DISABLED)
    T.bind("<Button>", lambda event: T.focus_set())
    new1.mainloop()





    

    

button1 = Button( root, text = "Add Face",background= '#336171',foreground = '#00ffff',command=new_window)
button2 = Button( root, text = "Recognize Face",background= '#336171',foreground = '#00ffff',command=recognize)
button3 = Button( root, text = "Clear Face Data",background= '#336171',foreground = '#00ffff',command = reset)
button4 = Button( root, text = "Exit",background= '#336171',foreground = '#00ffff',command = gui_exit)
button5 = Button( root, text = "HELP !",background= '#336171',foreground = '#00ffff',command = gui_help)




button1_canvas = canvas1.create_window( 70, 100,anchor = "nw",window = button1,height = 70, width = 150)
button2_canvas = canvas1.create_window( 70, 200,anchor = "nw",window = button2,height = 70, width = 150)
button3_canvas = canvas1.create_window( 70, 300,anchor = "nw",window = button3,height = 70, width = 150)
button4_canvas = canvas1.create_window( 70, 400,anchor = "nw",window = button4,height = 70, width = 150)
button5_canvas = canvas1.create_window( 590, 400,anchor = "nw",window = button5,height = 70, width = 150)


root.mainloop()
