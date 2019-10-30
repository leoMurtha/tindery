import tkinter as tk
from tkinter import *
import cv2
import numpy as np
from PIL import Image, ImageTk
import json
from person import Person
import io
import tinder_api
from time import sleep



class DisplayImage:

    def __init__(self, master, person):
        self.person = person
        self.images = iter([Image.open(io.BytesIO(img)) for img in person.download_images()])
        self.master = master
        self.master.geometry("1600x1000") #You want the size of the app to be 500x500
        self.master.resizable(0, 0) #Don't allow resizing in the x or y direction
        master.title("GUI")
        self.master.bind("<Button-1>", self.like)
        self.master.bind("<Button-2>", self.read_image)
        self.master.bind("<Button-3>", self.dislike)
        
        self.image_frame = Frame(master, borderwidth=0, highlightthickness=0, height=20, width=30, bg='white')
        self.image_frame.pack()
        
        self.image_label = Label(self.image_frame, highlightthickness=0, borderwidth=0)
        
        self.image_label.pack()
        self.dislike_user = Button(master, command=self.dislike, text="DISLIKE", width=17, default=ACTIVE, borderwidth=0)
        self.dislike_user.pack()
        self.next_image = Button(master, command=self.read_image, text="Next image", width=17, default=ACTIVE, borderwidth=0)
        self.next_image.pack()
        self.like_user = Button(master, command=self.like, text="LIKE", width=17, default=ACTIVE, borderwidth=0)
        self.like_user.pack()

        self.image_label.bind("<Button-1>", self.like)
        self.image_label.bind("<Button-2>", self.read_image)
        self.image_label.bind("<Button-3>", self.dislike)
        self.image_label.pack()
        
    def like(self, arg):
        self.person.like()    
        self.master.destroy()
        return True

    def dislike(self, arg):
        self.person.dislike()
        self.master.destroy()
        return False

    def display_image(self, event=None):
        self.imgt = ImageTk.PhotoImage(image=self.image)
        self.image_label.configure(image=self.imgt)

    def read_image(self, event=None):
        try:
            self.image = next(self.images)
            width, height = self.image.size
            max_height = 1000
            if height > max_height:
                resize_factor = max_height / height
                self.image = self.image.resize((int(width*resize_factor), int(height*resize_factor)), resample=Image.LANCZOS)
            #self.image = self.image.resize(1400, 800, resample=Image.LANCZOS)
            
            self.master.after(10, self.display_image)     
        except:
            print('Images for this user is over decide like or dislike')


if __name__ == "__main__":
    # with open('users_mock.json', mode='r') as f:
    #    recs = json.load(f)

    api = tinder_api.API()

    persons = []
    for i in range(4):
        persons.extend(api.get_recs_v2('pt-br'))
        sleep(3)

    total = len(persons)
    for i, person in enumerate(persons):
        print('Person: %s// total%s/%s' % (person.id, total, i))
        root = tk.Tk()
        GUI = DisplayImage(root, person)
        GUI.read_image()
        root.mainloop()
