import pygame as pg
from PIL import Image
def image_bottom_height(image,percent):
    raw_str = pg.image.tostring(image, "RGBA", False)
    img = Image.frombytes("RGBA", image.get_size(), raw_str)
    cropped_image=img.crop((0,img.height*percent,img.width,img.height))
    pixels=cropped_image.load()
    count=0
    countt=0
    listt_of_len=[]
    listt_of_len2=[]

    for i in range(cropped_image.height):
        for j in range(cropped_image.width):
            if pixels[j,i]==(0,0,0,0) :
                pixels[j,i]=(255,255,255,0)

    for i in range(cropped_image.height):
        for j in range(cropped_image.width):
                if pixels[j, i]==(255,255,255,0):
                    count+=1
                else:
                    break
        listt_of_len.append(count)
        count = 0
    for i in range(cropped_image.height):
        for j in range(cropped_image.width):
                if pixels[j, i] != (255, 255, 255, 0):

                    countt+=1
        listt_of_len2.append(countt)
        countt=0

    return min(listt_of_len),cropped_image.height,max(listt_of_len2)

def get_key(val,my_dict):
    for key, value in my_dict.items():
         if val == value:
             return key