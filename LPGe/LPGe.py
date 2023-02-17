# -*- coding: utf-8 -*-
""" ----------------------------------------------------------------------------------------------------------------------------------------------
    ---------------------------------------------------------- GEPAR research group --------------------------------------------------------------
    -------------------------------------------------------- University of Antioquia -------------------------------------------------------------
    ----------------------------------------------------------- Medellín, Colombia ---------------------------------------------------------------
    -------------------------------------------------------------- April, 2021 -------------------------------------------------------------------
    ----------------------------------------------------------------------------------------------------------------------------------------------
    --------------------------------------------- Authors: * David Stephen Fernández Mc Cann -----------------------------------------------------
    ------------------------------------------------------ * Carlos Alfonso Arbeláez Acevedo -----------------------------------------------------
    ----------------------------------------------------------------------------------------------------------------------------------------------
    -----------------------------------------------Project Name: License Plate Generator ---------------------------------------------------------
    ----------------------------------------------------------------------------------------------------------------------------------------------
    --------Description: LPGe is software that generates realistic license plates using synthetic plates. LPGe can generate plates----------------
    -------------------- with different attributes, like plate number, plate city, brightness, blurring, and color. LPGe was intended ------------
    -------------------- for the creation of databases, for which it has a function of random Generation.-----------------------------------------
    ----------------------------------------------------------------------------------------------------------------------------------------------
"""
""" --------------------------------------------------- 1. Libraries needed ---------------------------------------------------------------------- """
import gen_utils as gu         # Generator image functions
import pix2pix as p2p          # GAN arquitecture module
import PySimpleGUI as sg       # Interface module
import numpy as np             # Mathematical functions module
from PIL import Image          # Module for image processing
from PIL import ImageFilter    # Module for load Image filters
import io                      # Provides main facilities for dealing with various types of I/O
import random                  # Module for Random processes 
from os import mkdir           # Operating system functionalities module
import errno                   # Error detection module
    
""" ----------------------------------------- 2. Loading Pretrained Model ------------------------------------------------------------------------ """
OUTPUT_CHANNELS = 3                                                        # 3 channel image configuration by default        
generator = p2p.unet_generator(OUTPUT_CHANNELS, norm_type='instancenorm')  # Creating the generator object
generator.load_weights('./pretrainedmodel/LPGe/weightsLPGe')               # Loading model weights to out generator object 

""" ----------------------------------------- 3. Definition of random generator funtion ---------------------------------------------------------- """
def random_generator(cont,path):
      
    citys_path='citys.txt'                                       # Loading the file with all colombian cities  
    citys_list=[]                                                # Creating an empty list   
    with open(citys_path,'r',encoding='utf-8') as file:          # Loop for read the text file and create a list where each city is an element   
   
        # reading each line    
        for line in file:      
            #for word in line:            
                     citys_list.append(line[:-1]) 
    
    letras=["A","B","C","D","E","F","G","H","I","J",
            "K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]    # List with avalaible alphabet characters [A-Z]
    num=["1","2","3","4","5","6","7","8","9","0"]                               # List with avalaible number [0-9]   
    colors=['white','yellow']                                                   # List with avalaible colors                                         
    
    
    for j in range(0,cont):                   
        
    # Random generation for loop that creates and saves diferents license
    # Plates and show a progress bar.
        
        
        if sg.one_line_progress_meter(                                          # Progress bar object 
        'Loading...',   
        j,
        cont,
        orientation='h',
        bar_color=('#F47264', '#FFFFFF')
        ):

            a=random.choice(letras)                                             # Choosing random letters and number          
            b=random.choice(letras)
            c=random.choice(letras)
            d=random.choice(num)
            e=random.choice(num)
            f=random.choice(num)
            text_plate=a+b+c+d+e+f                                              # Concatenate all the plate text
            color=colors[random.randint(0,1)]                                   # Random color selection
            random_city=citys_list[random.randint(0,len(citys_list))]           # Random city selection           
            placa=gu.gen_placas(text_plate,random_city)                         # Syntethic plate generation   
            placa=gu.plate_color(placa, color)                                  # Syntethic plate color selection 
            placa0=gu.brightness(placa,random.randint(-100,100))                # Syntethic plate random bright modification
            
            
            placa0=Image.fromarray(np.uint8(placa0))                            # Converting Image to unit8 array
            placa0= placa0.resize((256*2,256))                                  # Image resizing                                            
            test_input = Image.fromarray(np.uint8(placa0))                      # Converting Image to unit8 array
            test_input=np.asarray(test_input)                                   # Converting Image to unit8 array
            test_input=p2p.normalize(test_input)                                # Image normalization
            prediction=p2p.generate_images(generator, test_input)               # Real plate generation
            prediction=np.asarray(prediction[0]*0.5+0.5)                        # Image preparition to save        
            test_input=Image.fromarray(np.uint8(prediction*255))                # Converting to a typical image with 255 max values
            test_input=test_input.resize((382,181))                             # Image resizing         
            filename=a+b+c+d+e+f+'.jpg'                                         # Creating image name or label
            test_input.save(path+'/'+filename)                                  # Saving image
            #This will Close The Window
        else:
            break;
    sg.one_line_progress_meter_cancel()                                         # Close the progress bar    
""" ---------------------------------------------------------- 4. Interface and model implementation ------------------------------------------------------------------------- """     
def main():
   # INTERFACE SETUP-------------------------------------------------------------------------------------------------------------------------------------------------------------    
    sg.theme('DarkAmber')                                                                                               # Change defalut interface colors                                 
    layout = [
        
        [sg.Text('Plate to generate:'), sg.InputText(size=(10,1),key='-IN-'),                                           # 'Plate to generate:' text, and input text configuration
         sg.Button('Generate', key="-SINGLE GENERATION-"),                                                              # Button Generate
         sg.Text(' Random Generation: '),sg.InputText(size=(10,1),key="n_random"),                                      # 'Random Generation:' text, and input text configuration
         sg.Button("Save Folder"),sg.Button('Generate', key="-RANDOM GENERATION-")],                                    # Button 'Save folder' and Button 'Generate'
        
        [sg.Text('Generated Plate',size=(48,1),justification="center"),                                                 # 'Generated Plate' text
         sg.Text('Altered Plate',size=(48,1),justification="center")],                                                  # 'Altered Plate' text
        
        [sg.Image(filename="", key="-IMAGE-",pad=(10,10)),sg.Image(filename="", key="-IMAGE-0",pad=(10,10))],           # Generated Image and Altered Image field
        [sg.Spin([i for i in range(-200,201)],pad=(0,5), initial_value=0,key="-BRIGHT SPIN-"),sg.Text('BRIGHT'),        # BRIGHT SPIN and text
         sg.Text('          '),sg.Spin([i for i in range(0,10)], initial_value=0,key="-BLUR SPIN-"),sg.Text('BLUR'),    # BLUR SPIN and text
         sg.Text('          '),sg.Checkbox("Yellow",size=(10, 1),key="-YELLOW-")],                                      # Yellow checkbox
            ]
    Logoslayout = [
                  [sg.Column([[sg.Image(key="-LOGO1-",pad=(10,10)),sg.Image(key="-LOGO2-",pad=(10,10)),                 # Image fields for logos
                               sg.Image(key="-LOGO3-",pad=(10,10))]],justification='c')]
                  ]
    
    MainLayout=[layout,Logoslayout]                                                        # Layout join                                                
    #VARIABLE FILENAMES----------------------------------------------------------------------------------------------------------------------------------------------------------
    file_path = './/images//'                                                              # Logo Images location                      
    logoFDI=file_path+'logofdi.jpg'                                                        # Logos file names            
    logoGEPAR=file_path+'logogepar.png'                                                     
    logoUDEA=file_path+'logoudea.png'
    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 
    window = sg.Window("LP-Ge", MainLayout,element_justification='c',size=(1000,450))      # SympleGui Window object Creation
    event, values = window.read(timeout=20)                                                # Read time setup
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #Initialization with plate AAA000 from xxxxxx--------------------------------------------------------------------------------------------------------------------------------
    placa= gu.gen_placas("AAA000","XXXXX")                                                 # Syntethic Plate generation     
    
    placa=Image.fromarray(np.uint8(placa))                                                 # Converting to PIL IMAGE 
    placa= placa.resize((256*2,256))                                                       # Resizing syntethic plate to introduce it into the generator 
    placa1= placa.resize((382,181))                                                        # Resizing to show in the image field 
    bio = io.BytesIO()                                                                     # io object to save the image bytes info                 
    placa1.save(bio, format="PNG")                                                         # Saving image bytes into bio object in PNG format         
    window["-IMAGE-"].update(data=bio.getvalue())                                          # Showing image             
    
    # GENERATION PROCESS---------------------------------------------------------------------------------------------------------------------------------------------------------
    test_input = Image.fromarray(np.uint8(placa))                                          # Syntehic plate to PIL IMAGE    
    test_input=np.asarray(test_input)                                                      # Syntehic plate to array
    test_input=p2p.normalize(test_input)                                                   # Normalization for the generator 
    prediction=p2p.generate_images(generator, test_input)                                  # Generator prediction from syntethic plate 
    prediction=np.asarray(prediction[0]*0.5+0.5)                                           # Obtaining the prediction from the generetor result 
    test_input=Image.fromarray(np.uint8(prediction*255))                                   # Converting the predicition to PIL Image 
    test_input=test_input.resize((382,181))                                                # Resizing to show in the image field 
    #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # IMAGE TO WINDOW VISUALIZATION PROCESS---------------------------------------------------------------------------------------------------------------------------------------   
    bio = io.BytesIO()                                                                     # io object to save the image bytes info                  
    test_input.save(bio, format="PNG")                                                     # Saving image bytes into bio object in PNG format 
    window["-IMAGE-0"].update(data=bio.getvalue())                                         # Showing image  
    #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    while True:
    # Interface While loop    
    
    #Logos--------------------------------------------------------------
        image1 = Image.open(logoUDEA)            #loading logo PIL image
        # IMAGE TO WINDOW VISUALIZATION PROCESS-------------------------
        bio = io.BytesIO()
        image1= image1.resize((70,100))
        image1.save(bio, format="PNG")
        window["-LOGO1-"].update(data=bio.getvalue())
        #---------------------------------------------------------------
        image1 = Image.open(logoFDI)            #loading logo PIL image
        # IMAGE TO WINDOW VISUALIZATION PROCESS-------------------------
        bio = io.BytesIO()
        image1= image1.resize((170,100))
        image1.save(bio, format="PNG")
        window["-LOGO2-"].update(data=bio.getvalue())
        #---------------------------------------------------------------       
        image1 = Image.open(logoGEPAR)           #loading logo PIL image
        # IMAGE TO WINDOW VISUALIZATION PROCESS-------------------------
        bio = io.BytesIO()
        image1= image1.resize((70,100))
        image1.save(bio, format="PNG")
        window["-LOGO3-"].update(data=bio.getvalue())
        event, values = window.read(timeout=20)
        #---------------------------------------------------------------  
    #-------------------------------------------------------------------
    #EVENT LECTURE-----------------------------------------------------------------------------------------------------------------------------------------------------
        if event == "Exit" or event == sg.WIN_CLOSED:
            break                                        #Exit interface
        if event == "Save Folder":
            save_path = sg.popup_get_folder("", no_window=True)                                                 # Saving the path were the random images will be stored
    # RANDOM GENERATION------------------------------------------------------------------------------------------------------------------------------------------------   
        if event == "-RANDOM GENERATION-":     
        # If there is no save_path selected, the images are saved in dir1 folder 
            try:
                random_generator(int(values["n_random"]),save_path)                                             # Random Generation with the especified values               
            except:
                try:
                    mkdir('dir1')                                                                               # Creating dir1 folder                                                                                                         
                    random_generator(int(values["n_random"]),'dir1')                                            # Random Generation with the especified values 
                except OSError as e:
                    if e.errno != errno.EEXIST: 
                        raise
                    else:    
                        random_generator(int(values["n_random"]),'dir1')                                        # Random Generation with the especified values     
              
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # SINGLE GENERATION------------------------------------------------------------------------------------------------------------------------------------------------   
        if event == "-SINGLE GENERATION-":
            try:
                placa= gu.gen_placas(values["-IN-"],values["-CITY-"])                                                  # Synthetic plate generation     
               
                if (values["-YELLOW-"]):                      
                                              
                     placa=gu.plate_color(placa, 'yellow')                                                             # Change the plate color
                     placa=Image.fromarray(np.uint8(placa))                                                            # Converting to PIL image           
                     
                # SOME PROCESSES ARE REAPEATED AND PREVIUSLY EXPLAINED, SO JUST THE CHANGED LINES WILL BE EXPLAINED 
                # IMAGE TO WINDOW VISUALIZATION PROCESS FOR SYNTHETIC PLATE--------------------------------------------------------------------------------------------
                placa=Image.fromarray(np.uint8(placa))                                                          
                placa= placa.resize((256*2,256))
                placa1= placa.resize((382,181))
                bio = io.BytesIO()
                placa1.save(bio, format="PNG")           
                window["-IMAGE-"].update(data=bio.getvalue())  
                #-------------------------------------------------------------------------------------------------------------------------------------------------------
                #GENERATION PROCESS-------------------------------------------------------------------------------------------------------------------------------------
                test_input = Image.fromarray(np.uint8(placa))
                test_input=np.asarray(test_input)                 
                test_input=p2p.normalize(test_input)
                prediction=p2p.generate_images(generator, test_input)
                prediction=np.asarray(prediction[0]*0.5+0.5)
                test_input=Image.fromarray(np.uint8(prediction*255))
                test_input=test_input.resize((382,181))
                #-------------------------------------------------------------------------------------------------------------------------------------------------------
                # IMAGE TO WINDOW VISUALIZATION PROCESS FOR ALTERED PLATE-----------------------------------------------------------------------------------------------
                bio = io.BytesIO()
                test_input.save(bio, format="PNG")
                window["-IMAGE-0"].update(data=bio.getvalue())
                #-------------------------------------------------------------------------------------------------------------------------------------------------------    
                #BRIGHT IF----------------------------------------------------------------------------------------------------------------------------------------------    
                if (values["-BRIGHT SPIN-"]):
                    # IMAGE TO WINDOW VISUALIZATION PROCESS FOR SYNTHETIC PLATE-----------------------------------------------------------------------------------------
                    placa=np.array(placa)
                    placa0 = gu.brightness(placa, values["-BRIGHT SPIN-"])                                                # Change the brightness by 'BRIGHT SPIN' Values
                    placa0=Image.fromarray(np.uint8(placa0))    
                    placa0= placa0.resize((256*2,256))
                    placa01=placa0.resize((382,181))
                    bio = io.BytesIO()
                    placa01.save(bio, format="PNG")           
                    window["-IMAGE-"].update(data=bio.getvalue())  
                    #----------------------------------------------------------------------------------------------------------------------------------------------------
                    #GENERATION PROCESS----------------------------------------------------------------------------------------------------------------------------------
                    test_input = Image.fromarray(np.uint8(placa0))
                    test_input=np.asarray(test_input)         
                    test_input=p2p.normalize(test_input)
                    prediction=p2p.generate_images(generator, test_input)
                    prediction=np.asarray(prediction[0]*0.5+0.5)
                    test_input=Image.fromarray(np.uint8(prediction*255))
                    test_input=test_input.resize((382,181))
                    #----------------------------------------------------------------------------------------------------------------------------------------------------
                    # IMAGE TO WINDOW VISUALIZATION PROCESS FOR ALTERED PLATE--------------------------------------------------------------------------------------------
                    bio = io.BytesIO()
                    test_input.save(bio, format="PNG")
                    window["-IMAGE-0"].update(data=bio.getvalue()) 
                    #----------------------------------------------------------------------------------------------------------------------------------------------------
                #--------------------------------------------------------------------------------------------------------------------------------------------------------
                #BLUR IF-------------------------------------------------------------------------------------------------------------------------------------------------        
                if (values["-BLUR SPIN-"]):
                    # IMAGE TO WINDOW VISUALIZATION PROCESS FOR SYNTHETIC PLATE------------------------------------------------------------------------------------------
                    placa=np.array(placa) 
                    placa0=Image.fromarray(np.uint8(placa))    
                    placa0= placa0.resize((256*2,256))
                    placa01=placa0.resize((382,181))
                    bio = io.BytesIO()
                    placa01.save(bio, format="PNG")           
                    window["-IMAGE-"].update(data=bio.getvalue())  
                    #----------------------------------------------------------------------------------------------------------------------------------------------------
                    #GENERATION PROCESS----------------------------------------------------------------------------------------------------------------------------------
                    test_input=placa 
                    test_input=p2p.normalize(test_input)
                    prediction=p2p.generate_images(generator, test_input)
                    prediction=np.asarray(prediction[0]*0.5+0.5)
                    test_input=Image.fromarray(np.uint8(prediction*255))
                    test_input=test_input.resize((382,181))
                    test_input = test_input.filter(ImageFilter.GaussianBlur(radius=(values["-BLUR SPIN-"])))                     # Blur the image by 'BRIGHT SPIN' Values
                    #----------------------------------------------------------------------------------------------------------------------------------------------------
                    # IMAGE TO WINDOW VISUALIZATION PROCESS FOR ALTERED PLATE--------------------------------------------------------------------------------------------
                    bio = io.BytesIO()
                    test_input.save(bio, format="PNG")
                    window["-IMAGE-0"].update(data=bio.getvalue())  
                    #----------------------------------------------------------------------------------------------------------------------------------------------------
                #--------------------------------------------------------------------------------------------------------------------------------------------------------
        # ERROR MESSAGE--------------------------------------------------------------------------------------------------------------------------------------------------
            except:
                sg.popup_error("Invalid entry")
                placa=gu.gen_placas('AAA000','Invalid')
      #------------------------------------------------------------------------------------------------------------------------------------------------------------------  
      #------------------------------------------------------------------------------------------------------------------------------------------------------------------  
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------    
    window.close()     # Close the window                      
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main() 