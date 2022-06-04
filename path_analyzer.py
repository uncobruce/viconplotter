
'''
    Class for path analysis (Vicon vs. odometry)
'''

import math

class Path():
    
    def __init__(self, file):
        self.file = file

    def geterror(self):
        '''
            Compute difference between desired and actual trajectories (e.g. heading error, deviation in distance etc.)
        '''
        pass
    
    def get_metrics(self):
        '''
            Get metrics for trajectory
        '''