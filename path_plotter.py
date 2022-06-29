
'''
    Functions for plotting Vicon motion capture system and QBii's odom data
'''

import math
import matplotlib.pyplot as plt
from matplotlib.transforms import Affine2D
import numpy as np
import pandas as pd
import random
import vicon_data_loader
import qbii_data_loader

# set x and y axis range for plot
#xlim = [-10, 10]
#ylim = [-2, 10]


def add_rect(x, y, theta, axes, label = False, color = 'b'):
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
    width = 5
    height = 1.8
    n = 0
    m = 0
    
    for a_x, a_y, a_t in zip(x, y, theta):
        
        rec = plt.Rectangle(xy=(a_x-width/2, a_y-height/2), width=width, height=height, 
                        color= color, alpha=0.9, fill=False,
                        transform=Affine2D().rotate_deg_around(*(a_x,a_y), a_t) + axes.transData)

        ## show rectangle at data
        if True:
            if m%15 == 0:    
                axes.add_patch(rec)
            m+=1
        
        
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

    fig_a = plt.figure(figsize=(8,7))
    axes_a = fig_a.add_axes([0.1,0.1,0.85,0.85])

    ## Method 1 of plotting orientation for square marker
    # axes_a.plot(x[:3], y[:3], color = 'r', lw =2, ls = '-.', marker =(4, 0, 45), markersize=30,\
    #     markerfacecolor = "none", markeredgecolor = 'b', markeredgewidth = 0.75)
    
    # axes_a.plot(x[2:], y[2:], color = 'r', lw =2, ls = '-.', marker =(4, 0, 78), markersize=30,\
    #     markerfacecolor="none", markeredgecolor = 'b', markeredgewidth = 0.75)

    axes_a.plot(x, y, color = 'black', alpha = 0.5, lw =2, ls = '-.', marker = 'o', markeredgecolor = 'black',  
        markersize= 5, markerfacecolor="r", markeredgewidth = 0.75)
    
    #axes_a.set_xlim(xlim)
    #axes_a.set_ylim(ylim)
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
        #i = random.randint(1, 99)
        i = 1
        fig_a.savefig('plot' + str(i) + '.png')


    
def plotmulti(x, y, theta, x1, y1, theta1, x2 = None, y2 = None, theta2 = None, num = 2, save = False):
    '''
        plot 2D path of rectangular robot

        x = list of x coordinates
        y = list of y coordinates
        theta = list of orientation (rz)
        num = number of plots in one figure
        save = save figure as png (bool)

        Note: angle = rotation in degrees anti-clockwise about xy.
    '''

    fig_a = plt.figure(figsize=(8,7))
    axes_a = fig_a.add_axes([0.1,0.1,0.85,0.85])

    axes_a.plot(x, y, color = 'r', alpha = 0.5, lw =2, ls = '-', marker = '.', markeredgecolor = 'black',  
        markersize= 5, markerfacecolor="r", markeredgewidth = 0.75, label = 'mocap')

    axes_a.plot(x1, y1, color = 'black', alpha = 0.5, lw =2, ls = '-', marker = '.', markeredgecolor = 'black',  
        markersize= 5, markerfacecolor="black", markeredgewidth = 0.75, label = 'qbii odom')


    ## for plotting commanded path
    if num ==3:

        axes_a.plot(x2, y2, color = 'orange', alpha = 0.5, lw =3, ls = '-', marker = '.', markeredgecolor = 'black',  
            markersize= 5, markerfacecolor="orange", markeredgewidth = 0.75, label = 'commanded')


        ## Plotting stadium
        # x2 = [0,0]
        # y2 = [0,100]
        # theta3 = []

        # axes_a.plot(x2, y2, color = 'orange', alpha = 0.5, lw =3, ls = '-', marker = '.', markeredgecolor = 'black',  
        # markersize= 5, markerfacecolor="orange", markeredgewidth = 0.75, label = 'commanded')

        # x2 = [-100,-100]
        # y2 = [100,0]
        # theta3 = []

        # axes_a.plot(x2, y2, color = 'orange', alpha = 0.5, lw =3, ls = '-', marker = '.', markeredgecolor = 'black',  
        # markersize= 5, markerfacecolor="orange", markeredgewidth = 0.75)

        # a = 50
        # b = 50
        # x0 = -50
        # y0 = 100
        # x2 = np.linspace(-a + x0, a + x0)
        # y2 = b * np.sqrt(1 - ((x2 - x0) / a) ** 2) + y0

        # axes_a.plot(x2, y2, color = 'orange', alpha = 0.5, lw =2, ls = '-', marker = '.', markeredgecolor = 'black',  
        # markersize= 5, markerfacecolor="orange", markeredgewidth = 0.75)
        
        # a = 50
        # b = 50
        # x0 = -50
        # y0 = 0
        # x2 = np.linspace(-a + x0, a + x0)
        # y2 = -b * np.sqrt(1 - ((x2 - x0) / a) ** 2) + y0

        # axes_a.plot(x2, y2, color = 'orange', alpha = 0.5, lw =2, ls = '-', marker = '.', markeredgecolor = 'black',  
        # markersize= 5, markerfacecolor="orange", markeredgewidth = 0.75)

        

    
    #axes_a.set_xlim(xlim)
    #axes_a.set_ylim(ylim)
    axes_a.grid(True, color='0.6')
    axes_a.set_facecolor('bisque')
    axes_a.set_title('Robot Trajectory')
    axes_a.set_xlabel('X (cm)')
    axes_a.set_ylabel('Y (cm)')   
    
    #add_rect(x, y, theta, axes_a, label = True)
    add_rect(x, y, theta, axes_a)
    add_rect(x1, y1, theta1, axes_a, color = 'green')
    #if num ==3:
        #add_rect(x2, y2, theta2, axes_a, color = 'purple')

    plt.legend()
    plt.show()
    plt.close()


def main():
    pass

if __name__ == '__main__':


    ## demo
    # x = np.array([0,0.1,0.1,-0.1,0,0,0.13,-0.12,0.02,1,2,3,3.4])
    # y = np.array([0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6])
    # theta = np.array([20,30,45,-22,20,123,6,0,0,25,0,-35,180])
    #plot2Dpath(x, y, theta)

    ## vicon
    file_vicon = './vicon_data/QBii_Square_2m_cw.csv'
    file_vicon1 = './vicon_data/QBii_Stadium_1m_ccw.csv'
    x1, y1, theta1 = vicon_data_loader.read_vicon(file_vicon1)
    #x1 = [i+1000 for i in x1]
    x1 = [i-843.5 for i in x1]
    vicon_data_loader.convert_units(x1, y1, theta1)

    #plot2Dpath(x1,y1,theta1)


    ## qbii
    file_qbii = './qbii_data/stadium_1m_ccw_vicon.csv'
    file_qbii1 = './qbii_data/square_2m_cw_vicon.csv'
    x2, y2, theta2 = qbii_data_loader.read_qbii(file_qbii)
    qbii_data_loader.convert_units(x2, y2, theta2)

    #plot2Dpath(x2,y2,theta2)


    ## 2m square 
    x3 = [0,200,200,0,0]
    y3 = [0,0,200,200,0]
    theta3 = []
    
    ## 1m stadium
    # x3 = [0,0]
    # y3 = [0,100]
    # theta3 = []

    ## plot data on same plot
    #plotmulti(x1,y1,theta1,x2,y2,theta2)
    plotmulti(x1,y1,theta1,x2,y2,theta2,x3,y3,theta3,num=3)

    