"""

Move to specified pose

Author: Daniel Ingram (daniel-s-ingram)
        Atsushi Sakai (@Atsushi_twi)
        Seied Muhammad Yazdian (@Muhammad-Yazdian)

P. I. Corke, "Robotics, Vision & Control", Springer 2017, ISBN 978-3-319-54413-7

"""

import matplotlib.pyplot as plt
import numpy as np
from random import random
from matplotlib.transforms import Affine2D
import math


class PathFinderController:
    """
    Constructs an instantiate of the PathFinderController for navigating a
    3-DOF wheeled robot on a 2D plane

    Parameters
    ----------
    Kp_rho : The linear velocity gain to translate the robot along a line
             towards the goal
    Kp_alpha : The angular velocity gain to rotate the robot towards the goal
    Kp_beta : The offset angular velocity gain accounting for smooth merging to
              the goal angle (i.e., it helps the robot heading to be parallel
              to the target angle.)
    """

    def __init__(self, Kp_rho, Kp_alpha, Kp_beta):
        self.Kp_rho = Kp_rho
        self.Kp_alpha = Kp_alpha
        self.Kp_beta = Kp_beta

    def calc_control_command(self, x_diff, y_diff, theta, theta_goal):
        """
        Returns the control command for the linear and angular velocities as
        well as the distance to goal

        Parameters
        ----------
        x_diff : The position of target with respect to current robot position
                 in x direction
        y_diff : The position of target with respect to current robot position
                 in y direction
        theta : The current heading angle of robot with respect to x axis
        theta_goal: The target angle of robot with respect to x axis

        Returns
        -------
        rho : The distance between the robot and the goal position
        v : Command linear velocity
        w : Command angular velocity
        """

        # Description of local variables:
        # - alpha is the angle to the goal relative to the heading of the robot
        # - beta is the angle between the robot's position and the goal
        #   position plus the goal angle
        # - Kp_rho*rho and Kp_alpha*alpha drive the robot along a line towards
        #   the goal
        # - Kp_beta*beta rotates the line so that it is parallel to the goal
        #   angle
        #
        # Note:
        # we restrict alpha and beta (angle differences) to the range
        # [-pi, pi] to prevent unstable behavior e.g. difference going
        # from 0 rad to 2*pi rad with slight turn

        rho = np.hypot(x_diff, y_diff)
        alpha = (np.arctan2(y_diff, x_diff)
                 - theta + np.pi) % (2 * np.pi) - np.pi
        beta = (theta_goal - theta - alpha + np.pi) % (2 * np.pi) - np.pi
        v = self.Kp_rho * rho
        w = self.Kp_alpha * alpha - controller.Kp_beta * beta

        if alpha > np.pi / 2 or alpha < -np.pi / 2:
            v = -v

        return rho, v, w


# simulation parameters
controller = PathFinderController(9, 15, 3)
dt = 0.01

# Robot specifications
MAX_LINEAR_SPEED = 15
MAX_ANGULAR_SPEED = 7

show_animation = True


def move_to_pose(x_start, y_start, theta_start, x_goal, y_goal, theta_goal):
    x = x_start
    y = y_start
    theta = theta_start

    x_diff = x_goal - x
    y_diff = y_goal - y

    x_traj, y_traj = [], []

    rho = np.hypot(x_diff, y_diff)
    while rho > 0.001:
        x_traj.append(x)
        y_traj.append(y)

        x_diff = x_goal - x
        y_diff = y_goal - y

        rho, v, w = controller.calc_control_command(
            x_diff, y_diff, theta, theta_goal)

        if abs(v) > MAX_LINEAR_SPEED:
            v = np.sign(v) * MAX_LINEAR_SPEED

        if abs(w) > MAX_ANGULAR_SPEED:
            w = np.sign(w) * MAX_ANGULAR_SPEED

        theta = theta + w * dt
        x = x + v * np.cos(theta) * dt
        y = y + v * np.sin(theta) * dt

        if show_animation:  # pragma: no cover
            plt.cla()
            plt.arrow(x_start, y_start, np.cos(theta_start),
                      np.sin(theta_start), color='r', width=0.1)
            plt.arrow(x_goal, y_goal, np.cos(theta_goal),
                      np.sin(theta_goal), color='g', width=0.1)
            plot_vehicle(x, y, theta, x_traj, y_traj)


def plot_vehicle(x, y, theta, x_traj, y_traj):  # pragma: no cover
    # Corners of triangular vehicle when pointing to the right (0 radians)
    p1_i = np.array([0.5, 0, 1]).T
    p2_i = np.array([-0.5, 0.25, 1]).T
    p3_i = np.array([-0.5, -0.25, 1]).T

    T = transformation_matrix(x, y, theta)
    p1 = np.matmul(T, p1_i)
    p2 = np.matmul(T, p2_i)
    p3 = np.matmul(T, p3_i)

    plt.plot([p1[0], p2[0]], [p1[1], p2[1]], 'k-')
    plt.plot([p2[0], p3[0]], [p2[1], p3[1]], 'k-')
    plt.plot([p3[0], p1[0]], [p3[1], p1[1]], 'k-')

    plt.plot(x_traj, y_traj, 'b--')

    # for stopping simulation with the esc key.
    plt.gcf().canvas.mpl_connect(
        'key_release_event',
        lambda event: [exit(0) if event.key == 'escape' else None])

    plt.xlim(0, 20)
    plt.ylim(0, 20)

    plt.pause(dt)


def transformation_matrix(x, y, theta):
    return np.array([
        [np.cos(theta), -np.sin(theta), x],
        [np.sin(theta), np.cos(theta), y],
        [0, 0, 1]
    ])


def main():

    for i in range(5):
        x_start = 20 * random()
        y_start = 20 * random()
        theta_start = 2 * np.pi * random() - np.pi
        x_goal = 20 * random()
        y_goal = 20 * random()
        theta_goal = 2 * np.pi * random() - np.pi
        print("Initial x: %.2f m\nInitial y: %.2f m\nInitial theta: %.2f rad\n" %
              (x_start, y_start, theta_start))
        print("Goal x: %.2f m\nGoal y: %.2f m\nGoal theta: %.2f rad\n" %
              (x_goal, y_goal, theta_goal))
        move_to_pose(x_start, y_start, theta_start, x_goal, y_goal, theta_goal)


def plot2Dpath(x, y, theta):
    '''
        plot 2D path of rectangular robot

        x = list of x coordinates
        y = list of y coordinates
        theta = list of orientation (rz)

        Note: angle = rotation in degrees anti-clockwise about xy.
    '''

    fig_a = plt.figure()
    axes_a = fig_a.add_axes([0.1,0.1,0.85,0.85])

    ## Method 1 of plotting orientation for square marker
    # axes_a.plot(x[:3], y[:3], color = 'r', lw =2, ls = '-.', marker =(4, 0, 45), markersize=30,\
    #     markerfacecolor = "none", markeredgecolor = 'b', markeredgewidth = 0.75)
    
    # axes_a.plot(x[2:], y[2:], color = 'r', lw =2, ls = '-.', marker =(4, 0, 78), markersize=30,\
    #     markerfacecolor="none", markeredgecolor = 'b', markeredgewidth = 0.75)

    axes_a.plot(x, y, color = 'black', alpha = 0.5, lw =2, ls = '-.', marker = 'o', markeredgecolor = 'black',  
        markersize= 5, markerfacecolor="r", markeredgewidth = 0.75)
    
    axes_a.set_xlim([-10, 10])
    axes_a.set_ylim([-1, 10])
    axes_a.grid(True, color='0.6')
    axes_a.set_facecolor = ('#FAEBD6')
    axes_a.set_title('Plot 1')
    axes_a.set_xlabel('X')
    axes_a.set_ylabel('Y')    # Add rectangles

    ## Method 2 of plotting orientation for rectangcular marker
    width = 0.6
    height = 0.3
    
    for a_x, a_y, a_t in zip(x, y, theta):
        
        rec = plt.Rectangle(xy=(a_x-width/2, a_y-height/2), width=width, height=height, 
                        color='b', alpha=0.9, fill=False,
                        transform=Affine2D().rotate_deg_around(*(a_x,a_y), a_t) + axes_a.transData)

        axes_a.add_patch(rec)

    plt.show()
    plt.close()


def plotmulti():
    
    fig_1, axes_1 = plt.subplots(figsize = (8,4), nrows = 1, ncols = 2)
    plt.tight_layout()

    # plot 1 
    #axes_1[0].plot(x,y)



if __name__ == '__main__':
    #main()

    x = np.array([0,0.1,0.1,-0.1,0,0,0.13,-0.12,0.02,1,2,3,3.4])
    y = np.array([0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6])
    theta = np.array([20,30,45,-22,20,123,6,0,0,25,0,-35])

    plotpath(x,y,theta)