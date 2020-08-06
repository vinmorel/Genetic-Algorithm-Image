#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 15:54:18 2019

@author: VincentMorel
"""
import numpy as np
#import cuda 

def Get_MAE(a,b):
    # initiate counter
    c = 0
    
    # for all pixels in width and height
    for i in range(a.shape[0]):
        for j in range(b.shape[1]):
            c += abs(np.subtract(a[i][j],b[i][j],dtype=np.int32))
    # numerator, denominator
    somme = c[0] + c[1] + c[2]
    pixels = a.shape[0] * a.shape[1]
    # calculation
    result = int((somme/pixels)*100)
    
    return result 


def Get_MSE(a,b):
    result =  (np.sqrt((np.subtract(a,b,dtype=np.int32))**2).sum())
    return result

if __name__ == '__main__':
    import cv2
        
    im1 = cv2.imread('/Users/VincentMorel/Desktop/H2019/Algorithme analyse de megadonnees/Projet/Genetic/Results/pikachu/result.jpg',1)
#    im2 = cv2.imread('/Users/VincentMorel/Desktop/H2019/Algorithme analyse de megadonnees/Projet/Genetic/Image/output10.jpg',1)
    src = cv2.imread('/Users/VincentMorel/Desktop/H2019/Algorithme analyse de megadonnees/Projet/Genetic/Source/pika.jpg',1)
    
    a = np.array(im1)
#    b = np.array(im2)
    c = np.array(src)
    

#    print(Get_MAE(a,c))
    print(Get_MSE(a,c))
#    print((Get_MAE(a,c)))
#    cv2.imread('/Users/VincentMorel/Desktop/H2019/Algorithme analyse de megadonnees/Projet/Genetic/Results/pikachutest/result.jpg')
#    print(((np.sqrt((np.subtract(a,c,dtype=np.int32))**2).sum())/(a.shape[1]*a.shape[0]))*100)

    
