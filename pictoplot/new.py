import pygame.image
from subprocess import call,Popen,PIPE

from cv2 import *
import fileinput
from PIL import Image
import platform
import sys 
from svg_to_gcode.svg_parser import parse_file
from svg_to_gcode.compiler import Compiler, interfaces
import aspose.words as aw
# sys.path.append('PICTOPLOT-MASTER/py-svg2gcode')


import sys
sys.path.insert(1, './inkscape')
import unicornlib


def img2bmp(imagepth,filename):
   
   doc = aw.Document()
   builder = aw.DocumentBuilder(doc)

   shapes = [builder.insert_image(imagepth)]

   # Calculate the maximum width and height and update page settings 
   # to crop the document to fit the size of the pictures.
   pageSetup = builder.page_setup
   pageSetup.page_width = max(shape.width for shape in shapes)
   pageSetup.page_height = sum(shape.height for shape in shapes)
   pageSetup.top_margin = 0;
   pageSetup.left_margin = 0;
   pageSetup.bottom_margin = 0;
   pageSetup.right_margin = 0;

   doc.save('./PBM images/'+str(filename[0])+".bmp");




def CovertToPBM(threshold,name):
    #Code to convert the bmp to a pbm
    print ("Converting output.bmp to output.pbm")
    #p1 = Popen(['convert', 'Output', '-d'], stdout=PIPE)
    #p2 = Popen(['mkbitmap', '-f', '2', '-s', '2', '-t', '0.48'], stdout=PIPE)
    call(["mkbitmap",'-x', "-t"+str(threshold),'./PBM images/'+str(name[0])+".bmp"])  



def ConvertToSVG(name):
    #Converting tmp/photo.pbm to tmp/photo.svg
    print ("Converting output.bmp to output.svg")
    #We -t200 handles the size of blobs we want to discard and it will convert to 40mmx40mm size
    #call(["potrace","--svg","-t200","-P 40mmx40mm","-W 40mm","-H40mm","--tight","tmp/photo.pbm"])
    call(["potrace","--svg","-t100","-P 40mmx40mm","-W 40mm","--tight",'./PBM images/'+str(name)+".bmp"]) 

def FixSvgHeader(name):
      #code to remove the pt
      print ("Removing pt and offsetting the svg ready for plotting")
      f =fileinput.FileInput('./PBM images/'+str(name)+".svg", inplace=True)
      for line in f:#loop through the lines
         if line.startswith("<g transform="):#find the transform line
            scale=0.0105000#Fit Page
            if platform.system()=="Windows":
               scale=0.009500#Looks Better
            else:
               scale=0.009500#Looks Better
            print('<g transform="translate(60.082978,20.809088) scale('+str(scale)+',-'+str(scale)+')"')#write the off set
         else:    
            print(line.replace('pt"', '"'))#remove the pt
      f.close()#Tidy up

def ConvertToGCode(name):
   #Convert svg to gcode data
   print ("Convert svg to gcode data")
   gcode_compiler = Compiler(interfaces.Gcode, movement_speed=1000, cutting_speed=300, pass_depth=5)

   curves = parse_file('./PBM images/'+str(name)+".svg") # Parse an svg file into geometric curves

   gcode_compiler.append_curves(curves) 
   gcode_compiler.compile_to_file('./Gcodes/'+name+'.gcode', passes=2)

   
     

     
      
#       #Writing the gcode file
#       print ("Writing the gcode file")
#       file = open("sample1.gcode","w") 
#       for c in e.context.codes:
#          file.write(c + '\n') 
#       file.close()




