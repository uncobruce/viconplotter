#!/usr/bin/env python
# license removed for brevity

import rospy
import sys
import actionlib
import csv
import math
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Twist, Pose
from std_msgs.msg import Empty
from nav_msgs.msg import Odometry
import time
from tf.transformations import euler_from_quaternion, quaternion_from_euler

class SquareMove(object):
    """
    This class is an abstract class to control a square trajectory on the turtleBot.
    It mainly declare and subscribe to ROS topics in an elegant way.
    """

    def __init__(self):

        # Declare ROS subscribers and publishers
        self.node_name = "square_move"
        self.odom_sub_name = "/odom"
        self.vel_pub_name = "/cmd_vel"
        self.vel_pub = None
        self.odometry_sub = None

        # ROS params
        self.pub_rate = 0.1
        self.queue_size = 2

        # Variables containing the sensor information that can be used in the main program
        self.odom_pose = None

    def start_ros(self):

        # Create a ROS node with a name for our program
        rospy.init_node(self.node_name, log_level=rospy.INFO)

        # Define a callback to stop the robot when we interrupt the program (CTRL-C)
        rospy.on_shutdown(self.stop_robot)

        # Create the Subscribers and Publishers
        self.odometry_sub = rospy.Subscriber(self.odom_sub_name, Odometry, callback=self.__odom_ros_sub, queue_size=self.queue_size)
        self.vel_pub = rospy.Publisher(self.vel_pub_name, Twist, queue_size=self.queue_size)

    def stop_robot(self):

        # Get the initial time
        self.t_init = time.time()

        # We publish for a second to be sure the robot receive the message
        while time.time() - self.t_init < 1 and not rospy.is_shutdown():
            
            self.vel_ros_pub(Twist())
            time.sleep(self.pub_rate)

        sys.exit("The process has been interrupted by the user!")

    def move(self):
        """ To be surcharged in the inheriting class"""

        while not rospy.is_shutdown():
            time.sleep(1)

    def __odom_ros_sub(self, msg):

        self.odom_pose = msg.pose.pose

    def vel_ros_pub(self, msg):

        self.vel_pub.publish(msg)

class SquareMoveOdom(SquareMove):
    """
    This class implements a semi closed-loop square trajectory based on relative position control,
    where only odometry is used. HOWTO:
     - Start the roscore (on the computer or the robot, depending on your configuration)
            $ roscore
     - Start the sensors on the turtlebot:
            $ roslaunch turtlebot3_bringup turtlebot3_robot.launch
     - Start this node on your computer:
            $ python move_square odom
    """

    def __init__(self):


        super(SquareMoveOdom, self).__init__()

        self.pub_rate = 0.1

    def get_z_rotation(self, orientation):

        (roll, pitch, yaw) = euler_from_quaternion([orientation.x, orientation.y, orientation.z, orientation.w])
        print roll, pitch, yaw
        return yaw
        
    def move_of(self, d, speed=0.5):

        x_init = self.odom_pose.position.x
        y_init = self.odom_pose.position.y

        # Set the velocity forward until distance is reached
        while math.sqrt((self.odom_pose.position.x - x_init)**2 + \
             (self.odom_pose.position.y - y_init)**2) < d and not rospy.is_shutdown():

            sys.stdout.write("\r [MOVE] The robot has moved of {:.2f}".format(math.sqrt((self.odom_pose.position.x - x_init)**2 + \
            (self.odom_pose.position.y - y_init)**2)) +  "m over " + str(d) + "m")
            sys.stdout.flush()

            msg = Twist()
            msg.linear.x = speed
            msg.angular.z = 0
            self.vel_ros_pub(msg)
            time.sleep(self.pub_rate)

        sys.stdout.write("\n")

    def turn_of(self, a, ang_speed=0.4):

        # Convert the orientation quaternion message to Euler angles
        a_init = self.get_z_rotation(self.odom_pose.orientation)
        print a_init

        # Set the angular velocity forward until angle is reached
        while (self.get_z_rotation(self.odom_pose.orientation) - a_init) < a and not rospy.is_shutdown():

            # sys.stdout.write("\r [TURN] The robot has turned of {:.2f}".format(self.get_z_rotation(self.odom_pose.orientation) - \
            #     a_init) + "rad over {:.2f}".format(a) + "rad")
            # sys.stdout.flush()
            # print (self.get_z_rotation(self.odom_pose.orientation) - a_init)

            msg = Twist()
            msg.angular.z = ang_speed
            msg.linear.x = 0
            self.vel_ros_pub(msg)
            time.sleep(self.pub_rate)

        sys.stdout.write("\n")

    def move(self):

        # Wait that our python program has received its first messages
        while self.odom_pose is None and not rospy.is_shutdown():
            time.sleep(0.1)

        # Implement main instructions
        # self.move_of(0.5)
        self.turn_of(math.pi/4)
        self.move_of(0.5)
        self.turn_of(math.pi/4)
        self.move_of(0.5)
        self.turn_of(math.pi/4)
        self.move_of(0.5)
        self.stop_robot()

def movebase_client():

    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = -2
    goal.target_pose.pose.position.y = -6
    goal.target_pose.pose.orientation.w = 1.0

    client.send_goal(goal)
    wait = client.wait_for_result()
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()

def write2csv():
    '''
        Create new Vicon csv file for time series plotting with PlotJuggler

        filename = Vicon csv data file
        freq = sampling frequency/frame rate of Vicon motion capturing trial
        tot_frame = total frame count for Vicon trial

    '''
    # open the file in the write mode
    f = open('./turttime1.csv', 'a')

    # create the csv writer
    writer = csv.writer(f)

    # write a row to the csv file
    writer.writerow(["Time (s)", "x (cm)", "y (cm)", "theta (rad)"])



def callback(msg):
    # open the file in the write mode
    f = open('./turttime1.csv', 'a')
    # create the csv writer
    writer = csv.writer(f)

    print(msg.pose.pose)

    (roll, pitch, yaw) = euler_from_quaternion([msg.pose.pose.orientation.x, msg.pose.pose.orientation.y, msg.pose.pose.orientation.z, msg.pose.pose.orientation.w])

    writer.writerow([time.time(), msg.pose.pose.position.x, msg.pose.pose.position.y, yaw])

    # close the file
    f.close()

if __name__ == '__main__':
    # try:
    #     rospy.init_node('movebase_client_py')
    #     result = movebase_client()
    #     if result:
    #         rospy.loginfo("Goal execution done!")
    # except rospy.ROSInterruptException:
    #     rospy.loginfo("Navigation test finished.")


    # set up node
    rospy.init_node('check_odometry')
    write2csv()

    # 100 Hz
    rate = rospy.Rate(100) 
    
    odom_sub = rospy.Subscriber('/odom', Odometry, callback)
    rospy.spin()

    # rospy.init_node('reset_odom')
    # # set up the odometry reset publisher
    # reset_odom = rospy.Publisher('/mobile_base/commands/reset_odometry', Empty, queue_size=10)
    # # # reset odometry (these messages take a few iterations to get through)
    # timer = time()
    # while time() - timer < 0.25:
    #     reset_odom.publish(Empty())
    
    #set up turtlebot publishing
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    
    
    move = Twist() # defining the way we can allocate the values
    move.linear.x = 0.3 # allocating the values in x direction - linear
    move.angular.z = 0.0  # allocating the values in z direction - angular

    #x=0
    while not rospy.is_shutdown(): 
        pub.publish(move)
        rate.sleep()
        #x+=1
        #if x>250:
        #    break 

    move.linear.x = 0.0 # allocating the values in x direction - linear
    move.angular.z = 0.0  # allocating the values in z direction - angular
    pub.publish(move)
    rate.sleep()





# def movebase_client():

#    # Create an action client called "move_base" with action definition file "MoveBaseAction"
#     client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
 
#    # Waits until the action server has started up and started listening for goals.
#     client.wait_for_server()

#    # Creates a new goal with the MoveBaseGoal constructor
#     goal = MoveBaseGoal()
#     goal.target_pose.header.frame_id = "map"
#     goal.target_pose.header.stamp = rospy.Time.now()
#    # Move 0.5 meters forward along the x axis of the "map" coordinate frame 
#     goal.target_pose.pose.position.x = 0.5
#    # No rotation of the mobile base frame w.r.t. map frame
#     goal.target_pose.pose.orientation.w = 1.0

#    # Sends the goal to the action server.
#     client.send_goal(goal)
#    # Waits for the server to finish performing the action.
#     wait = client.wait_for_result()
#    # If the result doesn't arrive, assume the Server is not available
#     if not wait:
#         rospy.logerr("Action server not available!")
#         rospy.signal_shutdown("Action server not available!")
#     else:
#     # Result of executing the action
#         return client.get_result()   

# # If the python node is executed as main process (sourced directly)
# if __name__ == '__main__':
#     try:
#        # Initializes a rospy node to let the SimpleActionClient publish and subscribe
#         rospy.init_node('movebase_client_py')
#         result = movebase_client()
#         if result:
#             rospy.loginfo("Goal execution done!")
#     except rospy.ROSInterruptException:
#         rospy.loginfo("Navigation test finished.")