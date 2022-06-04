import numpy as np
import pandas as pd
import math
import csv


def read_vicon(filename):
    '''
        Get x (mm), y (mm), theta (rad) data in 1d np.array from Vicon csv output
        
        filename = Vicon csv data file

        x = 1d np.array of x coordinate values (mm)
        y = 1d np.array of y coordinate values (mm)
        theta = 1d np.array of theta (rz) orientation values (rad)
       
    '''
    df = pd.read_csv(filename, header = 4)
    np_df = df.values
    
    x = np_df[:,5]
    y = np_df[:,6]
    theta = np_df[:,4]

    return x, y, theta


def convert_units(x, y, theta):
    '''
        Convert units of reading from mm to cm & rad to deg

        x = list of x coordinates (mm)
        y = list of y coordinates (mm)
        theta = list of orientation (rz - rad)   

        Note: input list parameters are modified by reference 

    '''
    x[:] = [float(reading/10) for reading in x]
    y[:] = [float(reading/10) for reading in y]
    theta[:] = [float(reading*180)/(math.pi) for reading in theta]


def frame2time(freq, tot_frame):
    '''
        Get time information for data points from frame rate

        freq = sampling frequency/frame rate of Vicon motion capturing trial
        tot_frame = total frame count for Vicon trial

        time = list of time values that corresponds to the given freq and tot_frame

    '''
    time = []
    #time.append(0) 

    for i in range(1,tot_frame+1):
        time.append(i//freq + (i-(freq*(i//freq)))/freq)
    
    return time

def write2csv(file, freq, tot_frame):
    '''
        Create new Vicon csv file for time series plotting with PlotJuggler

        filename = Vicon csv data file
        freq = sampling frequency/frame rate of Vicon motion capturing trial
        tot_frame = total frame count for Vicon trial

    '''
    x, y, theta = read_vicon(file)
    convert_units(x,y,theta)
    time = frame2time(100, len(x))

    with open('./time_series/time1.csv', 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Time (s)", "x (cm)", "y (cm)", "theta (deg)"])

        for i in range(len(time)):
            writer.writerow([time[i], x[i], y[i], theta[i]])



    



#file = './data/test1.csv'
#x, y, theta = read_vicon(file)
# convert_units(x,y,theta)

# print (x)
# print ('______________________')
# print (len(y))
# # print ('______________________')
# # print (theta)
# print ('______________________')
# time = frame2time(100, len(x))
# #print(time)
# print(time)



file = './data/test1.csv'
x, y, theta = read_vicon(file)
write2csv(file,100, len(x))