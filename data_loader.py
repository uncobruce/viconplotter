import numpy as np
import pandas as pd
import math

def read_vicon(filename):
    '''
        Get x (mm), y (mm), theta (rad) data in 1d np.array from Vicon csv output
        
        filename = Vicon csv data file
       
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

    '''
    x[:] = [float(reading/10) for reading in x]
    y[:] = [float(reading/10) for reading in y]
    theta[:] = [float(reading*180)/(math.pi) for reading in theta]
    


file = './test1.csv'
x, y, theta = read_vicon(file)
convert_units(x,y,theta)

# print (x)
# print ('______________________')
# print (y)
# print ('______________________')
# print (theta)
# print ('______________________')
# print(type(x))