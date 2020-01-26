# GeneticAlgorithmImage

> This program seeks to replicate as accurately as possible an image with a genetic algorithm-like process by drawing random ellipse mutations on a blank canvas and retaining mutations that reduce the most the distance between both work-in-progress and source image. 

## Results 
These examples demonstrate a timelapse of the image replication process at every iteration, where the best mutation is retained. 

![Showcase1](/header_animated.gif) ![source1](/Source/pika_source.jpg)  

![Showcase2](/header_animated_2.gif) ![source2](/Source/louis_source.png) 

MSE stands for Mean Squared Error, which is the distance calculation used in order to compare the work-in-progress (left) to the source image (right). It is sort of an euclidean distance, where every pixel RGB is compared between both images. 

## How it works

In short, the program creates at every iteration N mutations (random ellipses) stemming from the same parent. Whichever mutation improves the distance the most is kept, and the process is repeated M times. Even though the outcome is random, N and M determine the quality of the image produced since they allow for more exploration at the cost of longer calculation times. 

## Running it on your machine

You will need to install the following libraries :
- [Numpy 1.17.5](https://anaconda.org/conda-forge/numpy)
- [Pandas 0.25.3](https://anaconda.org/conda-forge/pandas)
- [OpenCV 4.0.1](https://anaconda.org/anaconda/opencv)

You will also need to change the directories in approx45.py to the ones that match your cloned repository.

When running it, the inputs are the following: 
- Path : Drag and drop your source image into console
- Project_name : The project name. Will create folders on computer to store info with this name.
- N_Ellipses : Number of ellipses that will be drawn in total on canvas. I recommend at least 500-1000 for a decent image.
- N_Mutations : Number of mutations per iteration. Exploratory variable, the more the better but also the longer.
- K : Number of dominant colors in source image. I recommend simple cartoonish images. For example, the pikachu has probably 5 colors (red, black, dark yellow, light yellow, brown)
- bkg : starting background color. Helps image replication so you don't need to waste ellipse iterations on filling background. 255 fot white, 0 for black. 
- verbose (optional) : 0 or 1 depending if you want to see calculations info in console. 

## Acknowledgments

Special thanks to [Muzkaw](https://youtu.be/LrEvoKI07Ww?t=25) for inspiring me to create my own version of this idea. 
