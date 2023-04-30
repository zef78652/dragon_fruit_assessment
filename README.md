# Dragonfruit Coding Challenge

## Image Generation
In the process of image creation for bacteria, random points around the center are generated and connected using the convex hull algorithm. The boundary points are then interpolated smoothly through Discrete Fourier transform. Sigma is set to (image size)/5 to ensure the image occupies 25% of the total image area..

![Bacteria]()

Luminescent dye images are created similarly, but with randomized mean (center of the dye) and a smaller sigma value of (image size)/50.

![Dye]()

## Image Compression
Run-length encoding (RLE) is used for compression, which is a lossless method that stores repetitive sequences as a single data value denoting the repeating block and its occurrence count. This allows the image to be precisely reconstructed upon decompression. However, RLE is most suitable for data with long runs of the same value and less effective on random or frequently changing data, potentially increasing space and time complexity.

In extreme cases with alternating pixels, applying RLE could require O(mn) space complexity, equivalent to no compression. Alternate methods like Huffman encoding or Lempel-Ziv compression might provide better compression

If in case the boundary of the bacteria is not smooth, then one of the above techniques might come out handy but for the sake of simplicity RLE is used for this coding challenge.

In general, the time complexity of RLE for a 2D image is proportional to the number of pixels in the image. Therefore, the time complexity of RLE for a 2D image can be expressed as O(mn), where m and n are the height and width of the image, respectively.

## Cancer Detection
After obtaining both images, overlapping pixels are counted. If the total percentage overlap exceeds 10%, cancer is detected; otherwise, the bacteria is deemed cancer-free.

## Image Size
The example images are sized at (1000 * 1000), or 8MB, for demonstration purposes, rather than the larger (100,000 * 100,1000), or 80GB, size. However, the method operates identically for both scales.