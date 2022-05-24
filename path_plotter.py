
'''
    Functions for plotting Vicon motion capture system's data
'''

import math
import matplotlib.pyplot as plt
from matplotlib.transforms import Affine2D
import numpy as np
import pandas as pd
import random
import data_loader

# set x and y axis range for plot
xlim = [-10, 10]
ylim = [-2, 10]


def add_rect(x, y, theta, axes, label = False):
    '''
        Method 2 of plotting orientation for rectangcular marker
        Adds rectangular box to each data point in existing plot axis

        x = list of x coordinates
        y = list of y coordinates
        theta = list of orientation (rz)   
        axes = matplotlib axis
        label = show label of data points (bool) 
        
        Note: a_t = rotation in degrees anti-clockwise about xy.
    '''
    width = 0.6
    height = 0.3
    n = 0
    
    for a_x, a_y, a_t in zip(x, y, theta):
        
        rec = plt.Rectangle(xy=(a_x-width/2, a_y-height/2), width=width, height=height, 
                        color='b', alpha=0.9, fill=False,
                        transform=Affine2D().rotate_deg_around(*(a_x,a_y), a_t) + axes.transData)

        axes.add_patch(rec)
        
        ## show data point labels
        if label:
            if n%3 == 0:    
                plt.text(a_x+0.2, a_y+0.2, f"({a_x}, {a_y}, {-a_t}\N{DEGREE SIGN})")  
            n+=1


def plot2Dpath(x, y, theta, save = False):
    '''
        plot 2D path of rectangular robot

        x = list of x coordinates
        y = list of y coordinates
        theta = list of orientation (rz)
        save = save figure as png (bool)

        Note: angle = rotation in degrees anti-clockwise about xy.
    '''

    fig_a = plt.figure(figsize=(6,4))
    axes_a = fig_a.add_axes([0.1,0.1,0.85,0.85])

    ## Method 1 of plotting orientation for square marker
    # axes_a.plot(x[:3], y[:3], color = 'r', lw =2, ls = '-.', marker =(4, 0, 45), markersize=30,\
    #     markerfacecolor = "none", markeredgecolor = 'b', markeredgewidth = 0.75)
    
    # axes_a.plot(x[2:], y[2:], color = 'r', lw =2, ls = '-.', marker =(4, 0, 78), markersize=30,\
    #     markerfacecolor="none", markeredgecolor = 'b', markeredgewidth = 0.75)

    axes_a.plot(x, y, color = 'black', alpha = 0.5, lw =2, ls = '-.', marker = 'o', markeredgecolor = 'black',  
        markersize= 5, markerfacecolor="r", markeredgewidth = 0.75)
    
    axes_a.set_xlim(xlim)
    axes_a.set_ylim(ylim)
    axes_a.grid(True, color='0.6')
    axes_a.set_facecolor('bisque')
    axes_a.set_title('Robot Trajectory')
    axes_a.set_xlabel('X (cm)')
    axes_a.set_ylabel('Y (cm)')   
    
    #add_rect(x, y, theta, axes_a, label = True)
    add_rect(x, y, theta, axes_a)

    plt.show()
    plt.close()
    
    if save:
        i = random.randint(1, 99)
        fig_a.savefig('plot' + str(i) + '.png')


def plotmulti():
    
    fig_1, axes_1 = plt.subplots(figsize = (8,4), nrows = 1, ncols = 2)
    plt.tight_layout()

    # plot 1
    # axes_1[0].set_title("Plot 1")
    # axes_1[0].set_xlabel("X")
    # axes_1[0].set_ylabel("Y")
    # axes_1[0].set_xlim([-10, 10])
    # axes_1[0].set_ylim([-1, 10])
    # axes_1[0].grid(True, color='0.6')
    # axes_1[0].set_facecolor('white')

    #axes_1[0].plot(x1, y1, color = 'black', alpha = 0.5, lw =2, ls = '-.', marker = 'o', markeredgecolor = 'black',  
    #    markersize= 5, markerfacecolor="r", markeredgewidth = 0.75)

    # plot 2
    # axes_1[1].set_title("Plot 2")
    # axes_1[1].set_xlabel("X")
    # axes_1[1].set_ylabel("Y")
    # axes_1[1].set_xlim([-10, 10])
    # axes_1[1].set_ylim([-1, 10])
    # axes_1[1].grid(True, color='0.6')
    # axes_1[1].set_facecolor('white')

    #axes_1[1].plot(x2, y2, color = 'black', alpha = 0.5, lw =2, ls = '-.', marker = 'o', markeredgecolor = 'black',  
    #    markersize= 5, markerfacecolor="r", markeredgewidth = 0.75)


def main():
    pass

if __name__ == '__main__':

    x1 = np.array([0,0.1,0.1,-0.1,0,0,0.13,-0.12,0.02,1,2,3,3.4])
    y1 = np.array([0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6])
    theta1 = np.array([20,30,45,-22,20,123,6,0,0,25,0,-35,180])

    x2 = np.array([0,0.1,0.1,-0.1,0,0,0.13,-0.12,0.02,1,2,3,3.4])
    y2 = np.array([0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6])
    theta2 = np.array([20,30,45,-22,20,123,6,0,0,25,0,-35,180])

    file = './test1.csv'
    x3, y3, theta3 = data_loader.read_vicon(file)
    data_loader.convert_units(x3, y3, theta3)

    #plot2Dpath(x3[:2000],y3[:2000],theta3[:2000])
    plot2Dpath(x1, y1, theta1)


    