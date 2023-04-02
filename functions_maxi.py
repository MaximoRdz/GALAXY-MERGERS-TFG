# Author: Máximo Rodríguez Herrero
# maximo.rodriguez@estudiante.uam.es
# Universidad Autónoma de Madrid

import numpy as np
import matplotlib.pyplot as plt

from scipy import stats
from ipywidgets import interactive


#plt.style.use(['science', 'notebook'])

def my_plot(image, figsize=(6, 6), percentiles=(0.25, 99.75), ax=None, cmap='inferno', show=True):
    """matplotlib customized imshow plot
    inputs: 
        - image
        - figsize: size adjustment
        - percentiles: plotting limits vmin and vmax
        - ax: if this plot is to be added on an existing axis (created outside the function)
        - cmap: color map style
        - show: calls plt.show if True"""
    # fig set to false if created outside the function
    fig = False 
    if not ax:
        # fig creation if ax not provided
        fig, ax = plt.subplots(figsize = figsize)
    
    show = ax.imshow(image, origin='lower',
                     vmin=np.nanpercentile(image, percentiles[0]),
                     vmax=np.nanpercentile(image, percentiles[1]),
                     cmap=cmap)
    # only add the colorbar if the fig has been created inside this function
    if fig:     
        plt.colorbar(show)
    if show:
        plt.show() 

    
def my_plot_log(image):
    """matplotlib customized imshow plot, fast way of creating a log plot
    if more complexity is needed use my_plot(log(image))"""
    fig, ax = plt.subplots(figsize=(10, 7))
    show = ax.imshow(np.log10(image), origin='lower',
                     vmin=np.nanpercentile(np.log10(image), 15),
                     vmax=np.nanpercentile(np.log10(image), 99.9),
                     cmap='inferno')
    plt.colorbar(show)
    plt.show() 

def cut_master_frames(master_frame, x1, y1, shape): 
    """frame resizing function
    inputs: 
        - master_frame: image to cut
        - x1, y1: row, column of the coordinates origin desired
        - shape: (x_size, y_size)"""
    x1 = int(x1)
    y1 = int(y1)
    # check for shape differences between current and desired sizes
    if master_frame.shape[0] != shape[0]:
        # cut out the desired rows 
        master_frame = master_frame[x1:x1+shape[0], :]
    else:
        pass
    if master_frame.shape[1] != shape[1]:
        # cut out the desired columns
        master_frame = master_frame[:, y1:y1+shape[0]]
    else:
        pass
    return master_frame

def sky_squares_median(row1, row2, column1, column2, image):
    """sky median counts calculation
    Given the image and the cut lines (horizotal and vertical) the result is 
    a grid such that the science object we want to observe is in the center rectangle 
    and the 8 adjacent rectangles will be used to compute the median value of the 
    sky counts
    inputs: 
        - row1, row2: row numbers for horizontal cuts
        - columns1, columns2: column number for vertical cuts
        - image: compute the sky counts from the image"""
    # three bottom rectangles
    sky1 = stats.mode(image[0:row1, 0:column1].flatten())[0]
    sky2 = stats.mode(image[0:row1, column1:column2].flatten())[0]  
    sky3 = stats.mode(image[0:row1, column2:].flatten())[0]
    # two middle rectangles
    sky4 = stats.mode(image[row1:row2, 0:column1].flatten())[0]
    sky5 = stats.mode(image[row1:row2, column2:].flatten())[0]        
    # three top rectangles
    sky6 = stats.mode(image[row2:, 0:column1].flatten())[0]
    sky7 = stats.mode(image[row2:, column1:column2].flatten())[0] 
    sky8 = stats.mode(image[row2:, column2:].flatten())[0]
    
    sky_modes = np.concatenate([sky1, sky2, sky3, sky4, sky6, sky7, sky8])
    # median count number of all the sky rectangles
    sky = np.nanmedian(sky_modes)
    return sky

def sky_histogram(data_dict, x1, x2, y1, y2):
    """visualization function
    Given the dictionary containing all of the science exposures
    it provides the count distribution of the image so the sky counts
    are visually checked before the sky substraction
    inputs:
        - data_dict: dictionary with the raw science exposures
        - x1, x2: row numbers for horizontal cuts
        - y1, y2: column number for vertical cuts"""
    for key, value in data_dict.items():
        print('Sky substraction: ' + key.upper())
        fig, axes = plt.subplots(1, len(value), figsize=(8, 3))
        
        for i, image in enumerate(value):
            # treat the zero values to avoid problems with the log scale
            image[image < 0] = np.nan
            sky0 = sky_squares_median(x1, x2, y1, y2, image)
            bins_0 = np.linspace(np.nanpercentile(image, .01), 
                                 np.nanpercentile(image, 99), 
                                 50) 

            axes[i].hist(image.flatten(), 
                         bins=bins_0,
                         color='b', 
                         histtype='barstacked', 
                         edgecolor='k', 
                         lw=.4, 
                         label=r'$R_{sky}$')
            axes[i].set_yscale('log')
            axes[i].axvline(sky0, color='r', label='sky median')
            axes[i].set_xlabel('Counts per sec [ADU/s]')
            axes[i].set_title(f'sky: {sky0:.2f} [ADU/s]')
            
        axes[0].set_ylabel('$dp/dR_{sky}$')
        axes[1].legend()
        plt.show()

# TODO preinicializar el corte con los valores anteriores
class SkyInteractive():
    """interactive plot to cut the science object out of the raw image and use 
    the surrounding rectangles to compute the sky"""
    def __init__(self, data):
        self.data = data
        self.fig, self.axes = plt.subplots(1, len(data), figsize=(8, 4))
        self.widget = interactive(self.update, 
                                  x1=(0,1023,1), 
                                  x2=(0,1023,1), 
                                  y1=(0,1023,1), 
                                  y2=(0,1023,1))
        display(self.widget)
        
    def sky_cut(self, x1, x2, y1, y2):
        for i, ax in enumerate(self.axes):
            # clean and plot a new image configuration after changing the slider 
            ax.clear()
            # high contrast plot for a better science object selection
            ax.imshow(self.data[i], origin='lower', 
                      vmin=np.nanpercentile(self.data[i], 50),
                      vmax=np.nanpercentile(self.data[i], 95),
                      cmap='inferno')
            # draw the cut lines
            ax.vlines([x1, x2], 0, 1023, color='w')
            ax.hlines([y1, y2], 0, 1023, color='w')
            ax.set_title(f'Frame: {i+1}')
    
    def update(self, x1=200, x2=900, y1=200, y2=750):
        """update the cut values from the plot interactive slider
        (default values set to x1=200, x2=900, y1=200, y2=750)"""
        self.sky_cut(x1, x2, y1, y2)
        self.fig.canvas.draw_idle()
        
    def get_cuts(self):
        """return the cut values x1, x2, y1, y2 from the 
        interactive figure dictionary"""
        return   self.widget.kwargs.values()
    
class CalibrationStars():
    """Class use to select manually from the plot the desired calibration stars
    Use: 
        Click one time on the left plot on the selected calibration star, this star will appear
        on the right plot, click one more time (now more accurately in the center of the star and 
        one last time on its raidus. Now that the centre location and the radius of this calibration 
        star is saved click again on the new calibration on the left plot
    input: 
        - data: image used
    output: 
        self.star_values -> dict containing star: (center(row, column), radius)"""
    def __init__(self, data):
        self.data = data
        # initiallize the figure
        self.fig, self.axes = plt.subplots(1, 2, figsize = (15, 8))
        self.fig.canvas.mpl_connect('button_press_event', self)
                
        my_plot(self.data, ax = self.axes[0])
        # position of the stars in the image (row, column)
        self.pos = []
        self.calib_stars = dict()
        # stars count
        self.n = 1
        
    def __call__(self, event):
        # rows i = y columns j = x
        x, y = int(event.xdata), int(event.ydata)
        self.dx, self.dy = 15, 15
        self.pos.append((y, x))
    
        if len(self.pos) == 1:
            my_plot(self.data[y-self.dy:y+self.dy, x-self.dx:x+self.dx], ax = self.axes[1])#, percentiles = (50, 95))
        elif len(self.pos) == 3:
            # after the third click on the image call the star_values to save the data and start again
            self.star_values()
        
    def star_values(self):
        radius = np.sqrt(np.sum((np.array(self.pos[2]) - np.array(self.pos[1]))**2))
        self.calib_stars[self.n] = np.array(self.pos[0]) + np.array(self.pos[1]) - np.array([self.dy, self.dx]), int(radius)
        self.n += 1
        # clear the position list starting the selection process again
        self.pos.clear()