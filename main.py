from GenerateImages import Generate_images
from Compression import Compression
import timeit

class Bacteria_Img_Analysis():
    
    
    if __name__ == "__main__":
        
        images = Generate_images()
        ed = Compression()
        size = 1000

        start = timeit.default_timer()
        
        print("Generating Bacteria Image")
        percentageAreaBacteria = 0
        while(percentageAreaBacteria<0.25):
            polygon,pixelsBacteria,percentageAreaBacteria = images.generate_bacteria()
            
        stop = timeit.default_timer()
        print('Time to generate Bacteria Image ', str(round(stop - start,2)) + " seconds") 

        sizeOfBacteriaImageBeforeComp = (len(pixelsBacteria)*len(pixelsBacteria[0])*8)/(size*size)
        print("Size of bacteria image before compression: " + str(round(sizeOfBacteriaImageBeforeComp,2)) + " MB")
        start = timeit.default_timer()
        pixelBacteriaCompressed = ed.imageEncoding(pixelsBacteria)
        stop = timeit.default_timer()
        print('Time to compress bacteria image ', str(round(stop - start,2)) + " seconds")  
        sizeOfBacteriaImageAfterComp = (len(pixelBacteriaCompressed)*len(pixelBacteriaCompressed[0])*8)/(size*size)
        print("Size of bacteria image after compression: " + str(round(sizeOfBacteriaImageAfterComp,2)) + " MB")
        images.displayImage(pixelsBacteria,percentageAreaBacteria,size,False)
        
        print("--------------------------------------")
        
        
        start = timeit.default_timer()
        print("Generating Image of Dye")
        
        pixelsCancer = images.generate_cancer()
        
        stop = timeit.default_timer()
        print('Time to generate Luminescent dye image ', str(round(stop - start,2)) + " seconds")  
        
        sizeOfCancerImageBeforeComp = (len(pixelsCancer)*len(pixelsCancer[0])*8)/(size*size)
        print("Size of Luminescent dye image before compression: " + str(round(sizeOfCancerImageBeforeComp,2)) + " MB")
        start = timeit.default_timer()
        pixelCancerCompressed = ed.imageEncoding(pixelsCancer)
        stop = timeit.default_timer()
        print('Time to compress Luminescent dye image ', str(round(stop - start,2)) + " seconds") 
        sizeOfCancerImageAfterComp = (len(pixelCancerCompressed)*len(pixelCancerCompressed[0])*8)/(size*size)
        print("Size of Luminescent dye image after compression: " + str(round(sizeOfCancerImageAfterComp,2)) + " MB")
        images.displayImage(pixelsCancer,0,size,True)
        
        pixelsBacteriaDecomp = ed.imageDecoding(pixelBacteriaCompressed)
        pixelsCancerDecomp = ed.imageDecoding(pixelCancerCompressed)
              
        print("--------------------------------------")

        overlap = 0

        for row in range(size):
            for col in range(size):
                if(pixelsBacteriaDecomp[row][col]==1 and pixelsCancerDecomp[row][col]==1):
                            overlap += 1 
        
        overlapPercentage = (overlap/(percentageAreaBacteria*size*size))*100
        
        if(overlapPercentage >=10):
            print("Bacteria body is " + str(overlapPercentage) + "% lit, thus cancer")
        else:
            print("Bacteria body is " + str(overlapPercentage) + "% lit, thus not cancer")
