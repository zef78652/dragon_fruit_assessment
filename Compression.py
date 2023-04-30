import numpy as np

#RLE is a lossless compression 
class Compression():
    
    def __init__(self,shape = (1000,1000)):
        
        self.shape = shape
    
    def imageEncoding(self,image):
     
        encoded = []
        count,previous = 0,None

        for row in image:
            for pixel in row:
                if((previous != None and previous != pixel) or (previous == pixel and count >= self.shape[0])):
                    encoded.append((count, previous))
                    previous=pixel
                    count=1
                elif(previous == pixel and count < self.shape[0]):
                    count += 1
                else:
                    previous = pixel
                    count+=1

        encoded.append((count, previous))
        return encoded


    def imageDecoding(self,encoded):

        decoded=[]
        for row,count in encoded:
            decoded.extend([count]*row)

        return np.array(decoded).reshape(self.shape)