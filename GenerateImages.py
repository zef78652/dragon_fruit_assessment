import cmath
import math
import random
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from matplotlib import colors


class Generate_images():
    
    def __init__(self):
        
        self.img_size = 1000
        
        self.mean = self.img_size/2
        self.sigma = self.img_size/5
        self.sigma_cancer = self.img_size/50
    
    #To find orientation of ordered triplet (p, q, r).
    def orientation(self, p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - \
            (q[0] - p[0]) * (r[1] - q[1])

        if val == 0:
            return 0
        elif val > 0:
            return 1
        else:
            return 2

    def convexHull(self,points):

        n = len(points)

        # Find the leftmost point
        minn = 0
        for i in range(1,len(points)):
            if points[i][0] < points[minn][0]:
                minn = i
            elif points[i][0] == points[minn][0]:
                if points[i][1] > points[minn][1]:
                    minn = i

        l = minn
        
        #Store vertices of convex hull
        hull = []
        p = l
        q = 0
        while(True):

            # Add current point to result 
            hull.append(p)

            q = (p + 1) % n

            for i in range(n):

                # If i is more counterclockwise 
                # than current q, then update q 
                if(self.orientation(points[p], 
                            points[i], points[q]) == 2):
                    q = i

            p = q

            # While we don't come to first point
            if(p == l):
                break

        return [(points[x][0],points[x][1]) for x in hull]

    # discrete Fourier Transform
    def dft(self,pointsIn1D):    
        return [sum(value * cmath.exp(2j*math.pi*index*l/len(pointsIn1D)) 
                    for index, value in enumerate(pointsIn1D)) for l in range(len(pointsIn1D))]

    # for each point, add N points in that Dimnesion
    def interpolatePoints(self,pointsIn1D, N):
        fourierValues = self.dft(pointsIn1D)
        midPoint = (len(pointsIn1D) + 1) // 2
        result = fourierValues[:midPoint] + [0]*(len(fourierValues)*N) + fourierValues[midPoint:]
        return [value.real / len(fourierValues) for value in self.dft(result)[::-1]]
    
    #Will generate a binary image of a polygon that represents bacteria
    def generate_bacteria(self,img_size = 1000):
    
        #Will use the convex hull algorithm to represent the outermost points that enclose the shape of bacteria, produced by points generated from a Gaussian distribution.
        boundary = self.convexHull([(random.gauss(self.mean, self.sigma), random.gauss(self.mean, self.sigma)) for _ in range(10)])

        #create a polygon by interpolation using DFT
        polygon = [list(vals) for vals in [self.interpolatePoints(pt, 10) for pt in zip(*boundary)]]
        
        #create a polygon obj
        polygon = Polygon([(polygon[0][l],polygon[1][l]) for l in range(len(polygon[0]))])

        count = 0

        rows, cols = (img_size, img_size)
        pixels = [[int(0) for _ in range(cols)] for _ in range(rows)]

        #Loop through each pixel in the image, and check if the pixel is contained within the polygon using Shapely's contains() method.
        for i in range(rows):
            for j in range(cols):
                if(polygon.contains(Point(i,j))):
                    pixels[i][j] = 1
                    count += 1

        #Calulate percentage of total area covered
        percentage = round(count/(rows*cols),2)
        return polygon,pixels,percentage
    
    #will generate image representing cancerous region
    def generate_cancer(self,img_size = 1000):

        polygons = []
        for _ in range(20):
            
            x,y = random.randrange(0, img_size),random.randrange(0, img_size)
            
            #Will use the convex hull algorithm to represent the outermost points that enclose the shape of bacteria, produced by points generated from a Gaussian distribution.
            boundary = self.convexHull([(random.gauss(x, self.sigma_cancer), random.gauss(y, self.sigma_cancer)) for _ in range(10)])

            ##create a polygon by interpolation using DFT
            polygon = [list(vals) for vals in [self.interpolatePoints(pt, 10) for pt in zip(*boundary)]]

            #create a polygon obj
            polygon = Polygon([(polygon[0][l],polygon[1][l]) for l in range(len(polygon[0]))])
            polygons.append(polygon)

        rows, cols = (img_size, img_size)
        pixels = [[int(0) for _ in range(cols)] for _ in range(rows)]
        
        #Loop through each pixel in the image, and check if the pixel is contained within the polygon, if yes, set it to be cancerous region and break
        for i in range(rows):
            for j in range(cols):
                point = Point(i,j)
                for polygon in polygons: 
                    if(polygon.contains(point)):
                        pixels[i][j] = 1
                        break
        
        return pixels
    
    def displayImage(self,pixels, percentageArea=0, imgSize = 1000, cancer = False):
        cmap = colors.ListedColormap(['white', 'black'])
        plt.imshow(pixels, cmap = cmap)
        plt.xlim([0, imgSize])
        plt.ylim([0, imgSize])
        if(cancer):
            plt.title("Luminescent dye image")
            plt.savefig('dye_img.png')
        else:
            plt.title("Bacteria Image, covers "+str(percentageArea*100)+" of total area")
            plt.savefig('bacteria_img.png')
        
        
    