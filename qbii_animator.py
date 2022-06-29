import random
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


plt.style.use('fivethirtyeight')

x_vals = []
y_vals = []

def plot_robot(x, y, theta):   
    ## plot robot marker 
    plt.plot(x.iloc[-1], y.iloc[-1], marker=(3, 0, theta), markersize=10, linestyle='None', label = 'QBii')


def plot_path(x, y, step):
    ## plot robot steps
    if len(x) < step:
        plt.plot(x[:-1], y[:-1], color = 'black', alpha = 0.5, lw =2, ls = '--', label = 'QBii path')
    else:
        plt.plot(x[-step:-1], y[-step:-1], color = 'black', alpha = 0.5, lw =2, ls = '--', label = 'QBii path')


def plot_lidar(x, y, step, laser_name):
    ## plot lidar readings
    if len(x) < step:
        plt.plot(x[:-1], y[:-1], color = 'red', alpha = 0.5, lw =2, ls = 'dotted', label = laser_name)
    else:
        plt.plot(x[-step:-1], y[-step:-1], color = 'red', alpha = 0.5, lw =2, ls = 'dotted', label = laser_name)


def update(i):
    data = pd.read_csv('data.csv')
    
    x = data['x_value']
    y1 = data['total_1']
    y2 = data['total_2']
    # laserx1 = data['laserx1']
    # lasery1 = data['lasery1']
    # laserx1 = data['laserx2']
    # lasery1 = data['lasery2']
    # laserx1 = data['laserx3']
    # lasery1 = data['lasery3']
    # laserx1 = data['laserx4']
    # lasery1 = data['lasery4']

    # clear old plot    
    plt.cla()
    # for stopping simulation with the esc key.
    plt.gcf().canvas.mpl_connect(
        'key_release_event',
        lambda event: [exit(0) if event.key == 'escape' else None])
    ## plot robot marker
    plot_robot(x,y1,0)
    ## plot previous steps
    plot_path(x,y1,50)
    
    ## laser 1
    #plot_lidar([num+10 for num in x],y1,30,"LF Laser")
    plot_lidar(x,[num+10 for num in y1],30,"LF Laser")
    ## laser 2
    #plot_lidar([num+10 for num in x],y2,30)
    ## laser 3
    #plot_lidar([num+10 for num in x],y2,30)
    ## laser 4
    #plot_lidar([num+10 for num in x],y2,30)
    
    plt.xlabel("x[m]")
    plt.ylabel("y[m]")
    # plt.axis("equal")
    # plt.grid(True)
    plt.legend(loc='upper left')
    plt.tight_layout()


ani = FuncAnimation(plt.gcf(), update, interval = 100)

plt.show()