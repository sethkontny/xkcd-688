from __future__ import division
from pylab import imread, ion, figure, set_cmap, imshow, axis, title
from numpy import zeros, arange, argwhere
import numpy as np
from scipy.misc import imresize
from time import sleep

from drawnow import drawnow

def sector_mask(shape=None, centre=(200, 300), percentage=0.25, radius=100):
    """
    Return a boolean mask for a circular sector. The start/stop angles in  
    `angle_range` should be given in clockwise order.
    """
    dc = 120
    angle_range = (dc, dc + percentage * 360)

    x, y   = np.ogrid[:shape[0],:shape[1]]
    cx, cy = centre
    tmin, tmax = np.deg2rad(angle_range)

    # ensure stop angle > start angle
    if tmax < tmin: tmax += 2*np.pi

    # convert cartesian --> polar coordinates
    r2 = pow(x-cx, 2) + pow(y-cy, 2)
    theta = np.arctan2(x-cx, y-cy) - tmin

    # wrap angles between 0 and 2*pi
    theta %= (2*np.pi)

    # circular mask
    circmask = r2 <= radius*radius

    # angular mask
    anglemask = theta <= (tmax-tmin)

    return circmask * anglemask

def draw_circle(percentage, image, r=70, center=(90, 148)):
    mask = sector_mask(shape=image.shape, percentage=percentage, radius=r, centre=center)
    image[mask] = 1
    return image

def draw_bars(panel_black, comic, height=400):
    base = 154
    for i in arange(3):
        bar_height = round(height * panel_black[i])
        comic[base-bar_height:base, 300+60*i:300+60*i+30] = 1

def draw_figure():
    # updating first panel
    number_black = argwhere(comic > BLACK).shape[0]
    percentage = number_black / n
    draw_circle(percentage, comic)

    # updating second panel
    panel_black = zeros(3)
    for i in arange(3):
        panel_black[i] = argwhere(comic[:, i*WIDTH:(i+1)*WIDTH] > BLACK).shape[0]
        panel_black[i] *= 1 / (WIDTH * HEIGHT)
    draw_bars(panel_black, comic)

    # updating the third panel
    resized = imresize(comic, 0.25)
    resized /= resized.max()
    rn, rm = resized.shape
    base_x, base_y = (80, 530)
    comic[base_x:base_x+rn, base_y:base_y+rm] = resized

if __name__ == "__main__":
    panels = 3
    WIDTH = 246
    BLACK = 0.2

    comic = imread('base.png')
    comic = 1 - comic
    HEIGHT = comic.shape[0]
    n = comic.shape[0] * comic.shape[1]

    # for drawnow
    S = 12
    ion()
    figure(figsize=(S, S/3))
    def update_image():
        set_cmap('binary')
        imshow(comic)#, interpolation='nearest')
        axis('off')
        title('Iteration %d' % (i+1))
        
    for i in arange(7):
        draw_figure()
        drawnow(update_image)
        sleep(1)
