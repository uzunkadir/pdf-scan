import shutil
import pytesseract 
from pdf2image import convert_from_path 
from glob import glob
import os
import pandas as pd 

from sys import path 
cwd = os.getcwd()
project_path = cwd.split("pdf-scan")[0]+"pdf-scan"


taranacak = pd.read_csv("taranacak.csv", header=None).values.tolist()
taranacak = [item for sublist in taranacak for item in sublist]

shutil.rmtree('taranmis')
shutil.rmtree('temp')


os.mkdir("taranmis")
os.mkdir("temp")

pytesseract.pytesseract.tesseract_cmd=r'C:/Program Files/Tesseract-OCR/tesseract.exe'


def images_deleter(yol):
    files = glob(yol)
    for f in files:
        os.remove(f)


paths = glob("pdf/*.pdf")

alltext=[]

from PyPDF2 import PdfFileReader



for i in range(len(paths)):   
    
    pdf = PdfFileReader(paths[i])
    page_count= int(pdf.getNumPages())
    
    for k in range(page_count):
        
        images = convert_from_path(paths[i],
                                   dpi=600,
                                   first_page=k,
                                   last_page=k,
                                   output_folder="temp",
                                   fmt="jpeg",
                                   size=(1653,2337),
                                   paths_only=True,
                                   single_file=True)[0]
    
        # for j in range(len(images)):
        # img=images[0]
        text = pytesseract.image_to_string(images,lang="tur")

        if any(x in text for x in taranacak):
            alltext.append(paths[i])
            shutil.copy(images, 'taranmis')
            
            old_name = "taranmis/" + images.split("\\")[-1]
            new_name = "taranmis/" + paths[i].split("/")[-1]+"--"+str(k)+".jpg"
            
            os.rename(old_name, new_name)
            
        print(f" pdf: {i+1}/{len(paths)} -- sayfa: {k+1}/{page_count} -- -- bulunan sayfa sayısı: {len(alltext)} ")
    images_deleter("temp/*")
