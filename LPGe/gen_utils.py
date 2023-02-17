# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 12:28:10 2021

@author: crlos
"""
import cv2
import random

letras=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
num=["1","2","3","4","5","6","7","8","9","0"]
colors=['white','yellow']


def plate_color(plate, color):
    rows,cols,channels = plate.shape               
    for z in range(0,rows):
        for x in range(0,cols):
            if plate[z][x][0] == 255:
                if color== 'yellow':
                    plate[z][x]=[234,170,0]
    return plate               
                    



def gen_placas(text,city):
    
        text=text.upper()
        city=city.upper()
        if len(city) > 15:
            city="OVERFLOW"

        a=text[0]
        b=text[1]
        c=text[2]
        d=text[3]
        e=text[4]
        f=text[5]
    
        #print("Su placa es:",a,b,c,d,e,f)
        path="./font/"
        dim = (50, 96)
        l1=cv2.imread(path+a+'.png')
        #print(path+a+'.png')

        l1 = cv2.resize(l1, dim, interpolation = cv2.INTER_NEAREST)
        l2=cv2.imread(path+b+'.png')
        l2 = cv2.resize(l2, dim, interpolation = cv2.INTER_NEAREST)
        l3=cv2.imread(path+c+'.png')
        l3 = cv2.resize(l3, dim, interpolation = cv2.INTER_NEAREST)
        l4=cv2.imread(path+d+'.png')
        l4 = cv2.resize(l4, dim, interpolation = cv2.INTER_NEAREST)
        l5=cv2.imread(path+e+'.png')
        l5 = cv2.resize(l5, dim, interpolation = cv2.INTER_NEAREST)
        l6=cv2.imread(path+f+'.png')
        l6 = cv2.resize(l6, dim, interpolation = cv2.INTER_NEAREST)
        logo=cv2.imread(path+'logo.png')
        s=cv2.imread(path+'space.png')
        s = cv2.resize(s, (7,96), interpolation = cv2.INTER_NEAREST)
        placa=cv2.hconcat([l1,s,l2,s,l3,s,logo,l4,s,l5,s,l6])
        #superposición para el marco
        marco = cv2.imread(path+'marco.png')
        
        rows,cols,channels = placa.shape
        #print(placa.shape)               
        marco[32:32+rows, 10:10+cols ] = placa
        #adding city  
        s=cv2.resize(s,(1,26),interpolation = cv2.INTER_NEAREST)
        city_img = s
        for i in range(0,len(city)):
                dim=(14,26)
                
                city_letter=city[i]
                if city_letter == '.':
                    city_letter= 'point'  
                if city_letter == ' ':
                    city_letter= 'space'
                if city_letter.isalpha() == False:
                     city_letter='space'        
                if city_letter == 'Ñ':
                     city_letter='N' 
                city_letter=cv2.imread(path+city_letter+'.png')   
                city_letter=cv2.resize(city_letter,dim,interpolation = cv2.INTER_NEAREST)              
                city_img=cv2.hconcat([city_img,city_letter,s,s,s,s,s,s])
        height, width, channels = city_img.shape
        print(city)
        marco[140:140+height,(191-width//2):(191-width//2)+width ] = city_img
                                   
        return marco

    
def random_generator(cont,cont2,path):

    for j in range(cont,cont2):
        a=random.choice(letras)
        b=random.choice(letras)
        c=random.choice(letras)
        d=random.choice(num)
        e=random.choice(num)
        f=random.choice(num)
        text_plate=a+b+c+d+e+f
        color=colors[random.randint(0,1)]
        placa=gen_placas(text_plate,color)    
        placa=brightness(placa,random.randint(-100,100))
        cv2.imwrite(path+str(j)+'.jpg',placa)
        #plt.imshow(placa)
        #plt.show()    
    
def brightness(input_image,value): 
    
    new_image= input_image
    cols, rows, channels = new_image.shape
    
    for x in range(0,cols):
        for y in range(0,rows):
            for z in range(0,channels):
                aux=new_image[x,y,z]+value
          
                if aux > 255:
                    new_image[x,y,z] =255
 
                elif aux < 0:
                    new_image[x,y,z] =0
                else:
                    new_image[x,y,z] =aux  
           
    return new_image   
 
