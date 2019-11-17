import os
import cv2
import json
import tkinter as tk
from tkinter import filedialog

def identifyFaces(file_path, display = False):
    #loads the image 
    try:
        if file_path.lower().endswith(('.png','.jpg','.jpeg')):
            color_img = cv2.imread(file_path)
        else:
            print("File type not yet supported, sorry :(")
    except Exception as e:
        raise e
    
    #scales the image
    h = color_img.shape[0] #actual image height
    w = color_img.shape[1] #actual image width
    if (w/h) > (1280/720): #scale based on width
        color_img = cv2.resize(color_img, (1280, int(1280*h/w)))
    else: #scale based on height
        color_img = cv2.resize(color_img,(int(720*w/h),720))

    #convert to grayscale
    gray_img = cv2.cvtColor(color_img,cv2.COLOR_BGR2GRAY) 

    #loads Haar cascade and its pretrained face detaction
    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml') 
    #detecting...
    faces = cascade.detectMultiScale(gray_img) 

    print('Found {0} face{1} in {2}'.format(len(faces),'s' if len(faces)>1 else '', os.path.basename(file_path)))
    
    #to display image with rectangle on faces
    if display:
        #draw the rectangles on faces
        for (x,y,w,h) in faces:
            cv2.rectangle(color_img,(x,y),((x+w),(y+h)),(118,146,0),5)

        #display the image
        cv2.imshow('Facial Detection',color_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    return json.dumps({'NumberOfFaces':len(faces)})

def main():
        #choose file input
        root = tk.Tk()
        root.withdraw() #hides the tk window
        img_path = filedialog.askopenfilename(initialdir = './photos',
        title = 'Choose an image',
        filetypes = (('JPEG','*.jpg;*.jpeg'),
        ('PNG','*.png'),
        ('all files','*.*')))

        output = identifyFaces(img_path,True)
        #make json file path
        json_path = ('').join(img_path.split('.')[:-1]) + '.json'
        answer = input('Save result to {}? yes/no: '.format(os.path.basename(json_path)))
        if answer.lower() in ('y','yes'):
            filehandle= open(json_path, 'w')
            filehandle.write(output)
            filehandle.close()
            print('Saved result to {}!'.format(os.path.basename(json_path)) )

if __name__ == "__main__": main()