# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 11:56:28 2020

@author: Vincent Morel
"""

import cv2
import math
import copy
import click
import random
import pickle
import numpy as np
from PIL import Image
from os import path
from os.path import isfile, join, split, splitext, abspath
from datetime import datetime


def Show_Img(img_array):
    image = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
    Image.fromarray(image).show()  

def Get_Colors(src_img,K):
    """
    Sample of colors from image using cv2 K-means color extraction.
    """
    Z = src_img.reshape((-1,3))
    Z = np.float32(Z)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret,label,center = cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
    
    # Dominant colors list from kmeans calc
    colors = np.uint8(center)
    return colors

def Save_to_Disk(logs, img_dir, img):
    """
    Save the logs of the image construction and the image itself inside the repository. 
    """
    base_path, file = split(img_dir)
    fname, ext = splitext(file)
    
    project_root_path = abspath(path.dirname(__file__))
    
    folders = {}
    folders['logs'] = 'txt'
    folders['results'] = 'png'
    
    for folder, ext in folders.items():
        output_dir = str(join(project_root_path,folder,f"{fname}.{ext}"))
        
        if isfile(output_dir):
            base_path, file = split(output_dir)
            fname, ext = splitext(file)
            now = datetime.now()
            dt_string = now.strftime("%H%M%S")
            fname += dt_string
        
            output_dir = join(base_path,fname)
        
        if folder == 'logs':
            with open(output_dir, "wb+") as f:
                pickle.dump(logs, f)  
            print("Saved logs at {output_dir}")
        else:
            cv2.imwrite(output_dir,img)
            print("Saved image at {output_dir}")
            
class Canvas:
    """
    The Canvas object initializes a blank image as a starting point for the main loop. 
    
    Parameters
    ----------
    src_img : (np array) 
        The input image in a numpy uint8 array. 
    """
    def __init__(self,src_img,K):
        self.h, self.w, self.c = src_img.shape
        self.blank_arr = np.full((self.h,self.w,3),255,np.uint8)
        self.blank_MSE = np.sqrt((np.subtract(src_img,self.blank_arr,dtype=np.int32))**2).sum()
        self.colors = Get_Colors(src_img,K).tolist()

class Parent():
    """
    The Parent object represents the parent image to stem from at each generation. The Get_MSE() 
    method is used calculate the distance between the input image and another candidate. The Mutate() 
    method is used to apply a random transformation to the parent image. 
    """
    def __init__(self,img, src_img):
        self.img_arr = img
        self.src_img = src_img
        self.img_arr_copy = copy.deepcopy(self.img_arr)
        self.h, self.w, self.c = self.img_arr.shape
        self.MSE = self.Get_MSE(self.src_img,self.img_arr)
        
    def Get_MSE(self, src_img, img):
        MSE = (np.sqrt((np.subtract(src_img,img,dtype=np.int32))**2).sum())
        return MSE

    def Mutate(self,N,colors):
        # Mutate from parent image
        self.img_arr = copy.deepcopy(self.img_arr_copy)
        #Initialize random ellipse cv2 variables
        clr = random.choice(colors)
        rot = random.randint(0,360)
        lt = random.randint(0,self.h)
        lg = random.randint(0,self.w)
        # Size (precision) by generation 
        s1 = random.randint(0,(self.h//(math.log10((N**6)+20))))
        s2 = random.randint(0,(self.w//(math.log10((N**6)+20))))          
        
        # draw on img_arr, save metrics
        cv2.ellipse(self.img_arr,(lg,lt),(s1,s2),rot,0,360,clr,-1)
        self.m_MSE = self.Get_MSE(self.src_img,self.img_arr)
        self.m_vars = [clr, rot, lt, lg, s1, s2]
        
        return self.img_arr, self.m_MSE, self.m_vars


@click.command()
@click.argument('img_dir')
@click.argument('k', type=int)
@click.option('--n_generations', type=int)
@click.option('--m_candidates', type=int)
@click.option('--verbose', type=int)

def main(img_dir,k,n_generations=200,m_candidates=100, verbose=0):
    """
    This function will start the genetic algorithm process. The program will stem m candidates
    from the parent image at each generation. Candidates are created by mutating the parent image.
    The mutation is the addition of an ellipse of random coordinates, sizes and color. Once the M
    candidates are created for the generation, the program will keep the best mutation and assign it
    as the new parent. The best candidate is the one which resembles the most the input image. This
    is measured by the MSE. The process loops for N generations.
        
    Parameters
    ----------
    img_dir : (string) 
        The path of the image to be duplicated using this genetic algorithm. 
    K : (int)
        The number of different colors to sample from during the mutations. Strongly suggested to 
        adjust this variable in accordance to your image. 
    n_iterations : (int), optional
        The number of generations to evolve from. The default is 200.
    n_mutations : (int), optional
        The number of mutations to create per generation. The default is 100.
    verbose : (bool), optional
        A boolean to decide if you want updates on the image being built at every 100th generation. 
        The default is 0. 
    """
    src_img = cv2.imread(img_dir)
    cvs = Canvas(src_img,k)
    
    darwin_sample = (cvs.blank_arr, cvs.blank_MSE)
    darwin_logs = []
    
    try:
        for generation in range(n_generations):
            p = Parent(darwin_sample[0], src_img)
            logs = []
    
            for mutation in range(m_candidates):
                m_arr, m_MSE, m_vars = p.Mutate(generation,cvs.colors)
                logs.append([m_arr, m_MSE, m_vars])
    
            logs = np.asarray(logs)
            MSEs = logs[:,1]
            best_mutation_idx = np.where(MSEs == np.amin(MSEs))[0][0]
            
            if np.amin(MSEs) <= darwin_sample[1]:
                darwin_sample = (copy.deepcopy(logs[best_mutation_idx][0]), logs[best_mutation_idx][1])
                darwin_logs.append([logs[best_mutation_idx,2], logs[best_mutation_idx,1]])
                
            print('MSE :', int(darwin_sample[1]),'\t', f"Progress : {generation+1}/{n_generations}")
    
            if verbose and generation % 100 == 0:
                Show_Img(darwin_sample[0])            
    
        Save_to_Disk(darwin_logs, img_dir,darwin_sample[0])
        Show_Img(darwin_sample[0])    
    
    except KeyboardInterrupt:
        Save_to_Disk(darwin_logs, img_dir,darwin_sample[0])
    

if __name__ == "__main__":
    main()
    