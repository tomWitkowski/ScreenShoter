import numpy as np
from scipy.stats import pearsonr


def flatten_screen(img: np.ndarray):
    """
    Rescale 3-dimensional image to gray-scale 2-dimensional image
    """
    return np.dot(img, np.array([0.2989, 0.5870, 0.1140]))


def fraction_to_one(x: np.ndarray):
    """
    Equal to:
    lambda x: 1 if x>0 else 0
    But much faster
    """
    s = np.sign(x)
    return (s+1)/2*np.abs(s)


def get_borders(im: np.ndarray, threshold: float = 0.6):
    """
    Returning a borders` indices of the main slide 
    if it doesn't take entire screen
    """
    # get differences between neighbour pixels
    im = im[1:,1:] - im[:-1,:-1]
    
    # and make all the same as 0
    im = fraction_to_one(im)

    # get a factor of being not the same in the line vertically and horizontally
    vmes, hmes = im.mean(0), im.mean(1)
    lenv, lenh = len(vmes), len(hmes)
    vind, hind = np.arange(0, lenv), np.arange(0, lenh)
    vmes = np.concatenate((vind.reshape(-1,1), vmes.reshape(-1,1)), 1)
    hmes = np.concatenate((hind.reshape(-1,1), hmes.reshape(-1,1)), 1)

    # get horizontal coordinates of indices, where the slideshow probably is
    h1 = hmes[(hmes[:,1]>threshold)*(hmes[:,0]<lenh/2)]
    h1 = h1[-1,0] if len(h1)>0 else 0
    h2 = hmes[(hmes[:,1]>threshold)*(hmes[:,0]>lenh/2)]
    h2 = h2[0,0] if len(h2)>0 else lenh-1

    # get vertical coordinates of indices, where the slideshow probably is
    v1 = vmes[(vmes[:,1]>threshold)*(vmes[:,0]<lenv/2)]
    v1 = v1[-1,0] if len(v1)>0 else 0
    v2 = vmes[(vmes[:,1]>threshold)*(vmes[:,0]>lenv/2)]
    v2 = v2[0,0] if len(v2)>0 else lenv-1
    
    h1, h2, v1, v2 = (int(x) for x in [h1, h2, v1, v2])
    
    # remove black borders
    
    while True:
        if vmes[v1,1] != 0:
            break
        v1 += 1
        
    while True:
        if vmes[v2,1] != 0:
            break
        v2 -= 1
        
    while True:
        if hmes[h1,1] != 0:
            break
        h1 += 1
        
    while True:
        if hmes[h2,1] != 0:
            break
        h2 -= 1
        
    return h1, h2, v1, v2


def get_slide(im: np.ndarray, threshold: float = 0.6):
    """
    Get a slide from the screen
    """
    img = flatten_screen(im)
    h1,h2, v1,v2 = get_borders(img, threshold)
    return im[h1:h2,v1:v2,:]


def the_same_slides(img: np.ndarray, img_new: np.ndarray) -> bool:
    """
    Returns boolean value whether the average of pixels
    vertically or horizontally differs significantly
    """
    im = flatten_screen(img[:,:,:3]) if len(img.shape) >= 3 else img
    im_new = flatten_screen(img_new[:,:,:3]) if len(img_new.shape) >= 3 else img_new
    
    # horizontal averages
    m0 = im.mean(0) 
    m0_new = im_new.mean(0) 
    
    m0 = m0[:min([len(m0),len(m0_new)])]
    m0_new = m0_new[:min([len(m0),len(m0_new)])]
    
    # vertical averages
    m1 = im.mean(1) 
    m1_new = im_new.mean(1) 
    
    m1 = m1[:min([len(m1),len(m1_new)])]
    m1_new = m1_new[:min([len(m1),len(m1_new)])]
    
    return max([abs(pearsonr(m0,m0_new)[0]), abs(pearsonr(m1,m1_new)[0])]) > 0.5