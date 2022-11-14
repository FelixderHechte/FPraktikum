#FFT quick library
import numpy as np
from PIL import Image
from PIL import ImageOps
import matplotlib.pyplot as plt

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

def FFTfiltering(Original, Filter, name, padding, size, type):

    original = Image.open(Original).convert('RGB')
    fftFilter = Image.open(Filter).convert('RGB')
    originalArray = np.flip(np.array(original), 0)
    fftFilterArray = np.array(fftFilter)

    greyOriginal = np.sum(originalArray, axis = 2)
    greyFilterVanilla = np.sum(fftFilter, axis = 2)
    greyFilterVanilla = greyFilterVanilla / np.max(greyFilterVanilla)

    greyFilter = np.fft.fftshift(greyFilterVanilla)

    originalFFTVanilla = np.fft.fft2(greyOriginal)
    originalFFT = np.multiply(originalFFTVanilla, greyFilter)

    originalBack = abs(np.fft.fft2(originalFFT))
    originalBack = np.flip(np.flip(originalBack, 0), 1)
    
    colormesh = np.multiply(abs(np.log(np.fft.fftshift(originalFFTVanilla))), np.fft.fftshift(greyFilter))
    originalFFTVanilla = abs(np.log(np.fft.fftshift(originalFFTVanilla)))

    xticks = np.linspace(0, greyOriginal.shape[0], 5)
    yticks = np.linspace(0, greyOriginal.shape[1], 5)
    
    for i,j in [[greyOriginal, "Original"], [colormesh, "FFT mit " + type], [originalBack, "Ruecktransformation"], [greyFilterVanilla, type + "filter"], [abs(originalFFTVanilla), "FFT"]]:
        
        fig, ax = plt.subplots(figsize=(size,size))

        ax.pcolormesh(i, cmap = 'magma')
        ax.set_title(j + r" ")
        ax.set_aspect('equal')
        
        filename = "Images/" + name + j + ".png"

        ax.set_yticks(yticks)
        ax.set_xticks(xticks)

        plt.xticks(color='w')
        plt.yticks(color='w')
    
        plt.tight_layout()
        plt.savefig(filename, dpi = 600)
        
        pad = [-padding, -padding, padding, padding]
        
        image = Image.open(filename)
        imageBox = ImageOps.invert(image.convert("RGB")).getbbox()
        imageBox = tuple(np.asarray(imageBox) + pad)
        
        image.crop(imageBox).save(filename)
        