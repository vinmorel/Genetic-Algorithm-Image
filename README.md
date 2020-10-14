# Genetic Algorithm Image Duplication

> This program seeks to replicate as accurately as possible an image with a genetic algorithm-like process by drawing random ellipse mutations on a blank canvas and retaining mutations that reduce the most the distance between both work-in-progress and source image. 

## Results 
These examples demonstrate a timelapse of the image replication process at every iteration, where the best mutation is retained. 

![Showcase1](/Assets/header_animated.gif) ![source1](/Assets/pika_source.jpg)  

![Showcase2](/Assets/header_animated_2.gif) ![source2](/Assets/louis_source.png) 

MSE stands for Mean Squared Error, which is the distance calculation used in order to compare the work-in-progress (left) to the source image (right). It is sort of an euclidean distance, where every pixel RGB is compared between both images. 

## How it works

In short, the program creates, at every iteration, N mutations (random ellipses) stemming from the same parent. Whichever mutation improves the distance the most is kept, and the process is repeated M times. Even though the outcome is random, N and M determine the quality of the image produced since they allow for more exploration at the cost of longer calculation times. 

## Running it on your machine

You will need to install the following libraries :
```
cd Genetic-Algorithm-Image
pip install -r requirements.txt
```

Run the script from CLI: 
```
python DuplicateMe.py img_dir  C:/.../img.png k [int] --n_generations [int] --m_candidates [int] --verbose [bool]
```
```
out[1]:
MSE : 5956339 	 Progress : 337/800 
MSE : 5956290 	 Progress : 338/800 
MSE : 5950198 	 Progress : 339/800 
... 
Saved logs at C:/.../logs.txt 
Saved image at C:/.../image.png 
```

The arguments are the following: 

```img_dir (string)``` :
The path of the image to be duplicated using this genetic algorithm. 
        
```K (int)``` :
The number of different colors to sample from during the mutations. Strongly suggested to 
adjust this variable in accordance to your image. 
        
```n_iterations (int), optional``` :
The number of generations to evolve from. The default is 200.
        
```n_mutations (int), optional``` :
The number of mutations to create per generation. The default is 100.
        
```verbose (bool), optional``` :
A boolean to decide if you want updates on the image being built at every 100th generation. 
The default is 0. 

## Acknowledgments

Special thanks to [Muzkaw](https://youtu.be/LrEvoKI07Ww?t=25) for inspiring me to create my own version of this idea. 
