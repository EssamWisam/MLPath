import numpy as np

def TTBD(img, t1, t2):                      # Two Threshold Binary Deomposition
    '''
    Takes an image and two thresholds and returns a binary image.
    '''
    img = (t1 <= img) & (t2 >= img)
    return img

def get_fractal_dimension(img):                                 
    '''
    Takes an image and returns the fractal dimension.
    '''

    # Slice image at multiples of k and add  pixels in each
    def boxcount(img, k):
        vertical_slices = np.add.reduceat(img, np.arange(0, img.shape[0], k), axis=0)
        boxCounts = np.add.reduceat( vertical_slices, np.arange(0, img.shape[1], k), axis=1)    # horizontal slice
        return len(np.where((boxCounts > 0) & (boxCounts < k*k))[0])        # How many boxes are not empty and not full (partial boxes)

    # Smaller dimension of image
    p = min(img.shape)

    # Largest n for which 2^n <= p
    n = int(np.floor(np.log2(p)))
   
    # Build successive box sizes (from 2**n down to 2**1)
    box_sizes = 2**np.arange(n, 1, -1)

    # Actual box counting with decreasing size
    partial_box_counts = [boxcount(img, box_size) for box_size in box_sizes]

    # Approximate the relation between log(box_sizes) and log(partial_box_counts) 
    # Then return the fractal dimension as the log partial box counts for very small box_sizes (np.log(box_sizes)=0), box_sizes=1
    coeffs = np.polyfit(np.log(box_sizes), np.log(partial_box_counts), 1)
    return -coeffs[0] if coeffs[0]==coeffs[0] else 0.0
