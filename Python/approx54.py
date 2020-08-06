#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 12:41:01 2019

@author: VincentMorel
"""
import os 
import numpy as np
import pandas as pd
import cv2
import random
from Get_MAE12 import Get_MSE
import math

# User inputs
path = str(input('Drag and drop image :')).strip("'")
project_name = str(input('Desired project name : '))
N_Ellipses = int(input('Number of ellipses : '))
N_Mutations = int(input('Number of mutations : '))
K = int(input('K : '))
bkg = int(input('Background color (White = 255 or Black = 0) : '))
#verbose = int(input('Verbose level (0 or 1) : '))

#path = '/Users/VincentMorel/Desktop/H2019/Algorithme analyse de megadonnees/Projet/Genetic/Source/color.jpg'
#project_name = 'test'
#N_Ellipses = 200
#N_Mutations = 75
verbose = 0

# Load source image
src = cv2.imread(path,1)
srcm = np.array(src)

# Height and width of src image
h = srcm.shape[0] # hauteur
w = srcm.shape[1] # longueur
v = 255

# Build new directories, if they dont exist
image_path = '/Users/VincentMorel/Desktop/H2019/Algorithme analyse de megadonnees/Projet/Genetic/Image/'
results_path = '/Users/VincentMorel/Desktop/H2019/Algorithme analyse de megadonnees/Projet/Genetic/Results/'
ite_path = '/Users/VincentMorel/Desktop/H2019/Algorithme analyse de megadonnees/Projet/Genetic/Iterations/'

if not os.path.exists(image_path+project_name) and verbose > 0:
    os.mkdir(image_path+project_name)
if not os.path.exists(results_path+project_name):
    os.mkdir(results_path+project_name)

# New blank image
blankm = np.full((h,w,3),bkg, np.uint16)
cv2.imwrite(image_path+'blank.jpg',blankm)
im = cv2.imread(image_path+'blank.jpg',1)

# Kmeans 
Z = src.reshape((-1,3))
Z = np.float32(Z)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
#K = 7

ret,label,center = cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

# Dominant colors list from kmeans calc
center = np.uint8(center)
print(center)

# Counter initialization
N = 0

# restore father image function
def restore(i,canvas):
    lt = int(data.iloc[i][0])
    lg = int(data.iloc[i][1])
    pos = (lg,lt)
    s1 = int(data.iloc[i][2])
    s2 = int(data.iloc[i][3])
    rot = int(data.iloc[i][4])
    b = int(data.iloc[i][5])
    g = int(data.iloc[i][6])
    r = int(data.iloc[i][7])
    clr = (b,g,r)
    img = cv2.ellipse(canvas,pos,(s1,s2),rot,0,360,clr,-1) 
    # output all images if verbose
    if verbose > 1:
        cv2.imwrite(image_path+project_name+'/output'+str(N)+'.jpg',img)
    # write image to disk        
    cv2.imwrite(image_path+project_name+'temp.jpg',img)
    # make copy of img for later
    img_c = np.array(cv2.imread(image_path+project_name+'temp.jpg',))
    copy = img_c.copy()  
    return copy

# main script
while N <= N_Ellipses:
    # initialize/Restore pandas ite_data
    ite_data = pd.DataFrame(columns=["lt", "lg","s1","s2","rot","b","g","r","MAE"])        
    
    # create results.txt file if it does not exist
    if not os.path.exists(results_path+project_name+'/results.txt'):
        open(results_path+project_name+'/results.txt',"x")
    
    # If results isnt empty, restore father image
    data = pd.read_csv(results_path+project_name+'/results.txt',sep=",", header=None, names = ["lt", "lg","s1","s2","rot","b","g","r","MAE"], dtype=int)
    if data.shape[0] > 0:
        # If results.txt at first line, restore father image on blank image
        if data.shape[0] == 1:
            i = 0
            canvas = blankm
            copy = restore(i,canvas)
        # If results.txt more than one line, restore father image on copy of image    
        elif data.shape[0] > 1:
            i = N-1
            canvas = copy
            restore(i,canvas)  
            
    # new mutations for generation X
    for i in range(N_Mutations):
        # random ellipse variables
        clr = random.choice(center.tolist())
        rot = random.randint(0,360)
        lt = random.randint(0,h)
        lg = random.randint(0,w)
        # Precision by generation 
        s1 = np.random.normal(0,(h//(math.log10((N**6)+20))))
        s2 = random.randint(0,(w//(math.log10((N**6)+20))))  
      
        # If no results yet, draw random ellipse on blank
        if data.shape[0] == 0:
            img = cv2.ellipse(blankm,(lg,lt),(s1,s2),rot,0,360,clr,-1)
            imgm = np.array(img)
            # Calc MAE
            new_MAE = Get_MSE(imgm,srcm) 
            if verbose > 0:
                print(lt,lg,s1,s2,rot,clr,new_MAE)
                print(new_MAE)
            # store values to RAM in dataframe
            ite_data = ite_data.append({'lt':lt, 'lg':lg, 's1':s1, 's2':s2, 'rot':rot, 'b':clr[0], 'g':clr[1], 'r':clr[2], 'MAE':new_MAE}, ignore_index=True)
            # restore blank file
            blankm = np.full((h,w,3),bkg, np.uint16)
            
        # If results, restore last father image and draw random on it
        if data.shape[0] > 0:
            # add random ellipse
            img = cv2.imread(image_path+project_name+'temp.jpg')
            img = cv2.ellipse(img,(lg,lt),(s1,s2),rot,0,360,clr,-1)
            imgm = np.array(img)
            # Calc MAE
            new_MAE = Get_MSE(imgm,srcm)
            if verbose > 0:
                print(lt,lg,s1,s2,rot,clr,new_MAE)
                print(new_MAE)
            # store values to RAM in dataframe
            ite_data = ite_data.append({'lt':lt, 'lg':lg, 's1':s1, 's2':s2, 'rot':rot, 'b':clr[0], 'g':clr[1], 'r':clr[2], 'MAE':new_MAE}, ignore_index=True)
            # restore father image
            img = copy
            
    # Write ellipse values with smallest MAE to results.txt
    sort = ite_data.sort_values("MAE")
    with open(results_path+project_name+'/results.txt',"a+") as result_file:
        result_file.write(str(int(sort.iloc[0][0]))+','+str(int(sort.iloc[0][1]))+','+str(int(sort.iloc[0][2]))+','+str(int(sort.iloc[0][3]))+','+str(int(sort.iloc[0][4]))+','+str(int(sort.iloc[0][5]))+','+str(int(sort.iloc[0][6]))+','+str(int(sort.iloc[0][7]))+','+str(int((sort.iloc[0][8]/(h*w))*100)))
        result_file.write('\n')
    # prints to kernel
    if verbose == 0:
        print(N,int(sort.iloc[0][0]),int(sort.iloc[0][1]),int(sort.iloc[0][2]),int(sort.iloc[0][3]),int(sort.iloc[0][4]),int(sort.iloc[0][5]),int(sort.iloc[0][6]),int(sort.iloc[0][7]),int((sort.iloc[0][8]/(h*w)*100)))
    # counter +1
    N += 1


# After loop -> Draw result
canvas = np.full((h,w,3),255, np.uint16)
canvas_data = pd.read_csv(results_path+project_name+'/results.txt',sep=",", header=None, names = ["lt", "lg","s1","s2","rot","b","g","r","MAE"], dtype=int)

for i in range(data.shape[0]):
    lt = int(data.iloc[i][0])
    lg = int(data.iloc[i][1])
    pos = (lg,lt)
    s1 = int(data.iloc[i][2])
    s2 = int(data.iloc[i][3])
    rot = int(data.iloc[i][4])
    b = int(data.iloc[i][5])
    g = int(data.iloc[i][6])
    r = int(data.iloc[i][7])
    clr = (b,g,r)
    
    img = cv2.ellipse(blankm,pos,(s1,s2),rot,0,360,clr,-1)
    
cv2.imwrite(results_path+project_name+'/result.jpg',img)


