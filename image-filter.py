from tkinter import *
import tkinter as tk
from tkinter import filedialog
import os
import cv2 as cv
from numpy.core.fromnumeric import size
 
class Filtering:

    def __init__(self, master):
        master.title("이미지 전처리")
        master.geometry("500x400") 
        # master.grid_columnconfigure(4, minsize = 100)
        
        self.label=Label(master, text='이미지 열기 : ').grid(row = 1, column = 1)
        
        self.ent=Entry(master, textvariable = t1).grid(row = 1, column = 2)
        self.btnBrowse=Button(master, text='열기' , command=self.browseimg).grid(row = 1, column = 3)        
        self.btnPreviewImage=Button(master, text='미리보기', command=self.previewimg).grid(row = 1, column= 4)
        
        self.ckb = Checkbutton(master, text = '크기조절 : ', variable = resizeChk, onvalue = 1).grid(row = 2, column = 1)
        self.entx = Entry(master, textvariable = resize_x).grid(row = 2, column = 2)
        self.extx = Label(master, text = 'X').grid(row = 2, column = 3)
        self.exty = Entry(master, textvariable = resize_y).grid(row = 2, column = 4)

        self.noiseChk = Checkbutton(master, text = '노이즈 제거', variable = noiseVar, onvalue = 1).grid(row = 4, column = 1)

        self.bgrmChk = Checkbutton(master, text = '배경제거', variable = bgrmVar, onvalue = 1).grid(row = 5, column = 1)

        self.binaryChk = Checkbutton(master, text = '이진화', variable = binaryVar, onvalue = 1).grid(row = 6, column = 1)

        self.btnResult = Button(master, text = '효과 미리보기', command = self.Filter).grid(row = 7, column = 1)

        self.btnSave = Button(master, text = '저장', command = self.saveFilter).grid(row = 8, column = 1)

    def browseimg(self):
        global img
        self.fln=filedialog.askopenfilename(initialdir=os.getcwd(), title='Browse Image File', filetypes=(('JPG Image', '*.jpg'), ('PNG Image', '*.png'), ('All Files', '*.*')))
        t1.set(self.fln)
        img=self.fln

    def previewimg(self):
        self.read=cv.imread(img, cv.IMREAD_UNCHANGED)
        cv.imshow('Source Image', self.read)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def Filter(self):
        self.read=cv.imread(img, cv.IMREAD_UNCHANGED)
        self.result = self.read.copy()
        if resizeChk.get() == 1:
            self.result = cv.resize(self.result, (resize_x.get(), resize_y.get()))
            print("resized!!")
        # elif rgbChk.get() == 1:
        #     if rgbVar == 1:
        #         # cv.cvtColor(self.read, cv.)
        #     elif rgbVar == 2:
        #         # 
        #     elif rgbVar == 3:
        if noiseVar.get() == 1:
            self.result = cv.fastNlMeansDenoisingColored(self.result, None, 15, 15, 5, 10)
            print("denoised!!")
        if bgrmVar.get() == 1:
            self.result = cv.GaussianBlur(self.result, (5, 5), 0)
        if binaryVar.get() == 1:
            gray = cv.cvtColor(self.result, cv.COLOR_BGR2GRAY)
            _, self.result = cv.threshold(gray, 0, 255, cv.THRESH_BINARY)
        cv.imshow('Filtered Image', self.result)
        cv.waitKey(0)
        cv.destroyAllWindows()

        global final_img
        final_img = self.result.copy()

    def saveFilter(self):
        self.save = final_img

        self.write_im = filedialog.asksaveasfilename(title = '이미지 저장', initialdir = os.getcwd, filetypes=(('JPG Image', '*.jpg'), ('PNG Image', '*.png'), ('All Files', '*.*')))
        cv.imwrite(self.write_im, self.save)

root = Tk()
t1 = StringVar()

resizeChk = IntVar()

resize_x = IntVar()
resize_y = IntVar()

rgbChk = IntVar()
rgbVar = IntVar()

noiseVar = IntVar()

bgrmVar = IntVar()

binaryVar = IntVar()

filter = Filtering(root)
root.mainloop()