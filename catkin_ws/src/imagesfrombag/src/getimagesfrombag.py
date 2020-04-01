#!/usr/bin/python

# Extract images from a bag file.
#
# Original author: Thomas Denewiler (http://answers.ros.org/users/304/thomas-d/)

# Start up ROS pieces.
PKG = 'imagesfrombag'
import roslib; roslib.load_manifest(PKG)
import rosbag
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

# Reading bag filename from command line or roslaunch parameter.
import os
import sys

class ImageCreator():

    image_type = ".tif"
    desired_topic = {'left_raw':'/camera_array/cam0/image_raw',
                'right_raw':'/camera_array/cam1/image_raw',
                'ir':'/flir_boson/image_raw'
                #,'depth_map': '/zed_node/depth/depth_registered_drop'
                }
    index_in_filename = True
    index_format = "06d"
    image_index = dict.fromkeys(desired_topic.keys(), 0) #[0]*len(desired_topic)

    # Must have __init__(self) function for a class, similar to a C++ class constructor.
    def __init__(self):
        # Get parameters when starting node from a launch file.
        '''if len(sys.argv) < 1:
            save_dir = rospy.get_param('save_dir')
            filename = rospy.get_param('filename')
            rospy.loginfo("Bag filename = %s", filename)
        # Get parameters as arguments to 'rosrun my_package bag_to_images.py <save_dir> <filename>', where save_dir and filename exist relative to this executable file.
        else:
            save_dir = os.path.join(sys.path[0])
            filename = os.path.join(sys.argv[2])
            rospy.loginfo("Bag filename = %s", filename)
        '''
        # save_dir = os.path.join(sys.path[1])
        filename = os.path.join(sys.argv[1])
        rospy.loginfo("Bag filename = %s", filename)
        # rospy.loginfo("Save Directory = %s", save_dir)
        # Use a CvBridge to convert ROS images to OpenCV images so they can be saved.
        self.bridge = CvBridge()
        bagname = (filename.split('/')[-1]).split('.bag')[0]
        save_dir = filename.split('.bag')[0]
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        #.strip('/')[-1]
        # Open bag file.
        with rosbag.Bag(filename, 'r') as bag:
            for topic, msg, t in bag.read_messages():
                #topic_parts = topic.split('/')
                # first part is empty string
                # print(topic)
                # print(self.desired_topic.values())
                if topic in self.desired_topic.values():
                    # hack , assuming the values are unique as supposed to
                    # definition of dict (as in this case)
                    # being lazy today, will add for loop and checking conditions some day
                    topic_sub_location = list(self.desired_topic.keys())[list(self.desired_topic.values()).index(topic)]
                    topic_dir_name = bagname +'_' + topic_sub_location
                    tmp_save_dir = save_dir + '/'+ topic_dir_name
                    if not os.path.exists(tmp_save_dir):
                        os.makedirs(tmp_save_dir)

                    try:
                        cv_image = self.bridge.imgmsg_to_cv2(msg)
                    except CvBridgeError, e:
                        print e
                    timestr = "%.3f" % msg.header.stamp.to_sec()
                    if self.index_in_filename:
                        image_name = str(save_dir) +'/'+topic_dir_name +"/" + bagname +'_{}'.format(topic_sub_location)+ "_" + format(self.image_index[topic_sub_location], self.index_format) + "-" + timestr + self.image_type
                    else:
                        image_name = str(save_dir) +'/'+topic_dir_name + "/" + bagname +'_{}'.format(topic_sub_location) + "_" + timestr + self.image_type
                    #print image_name
                    cv2.imwrite(image_name, cv_image)

                    self.image_index[topic_sub_location] += 1
                    if self.image_index[topic_sub_location] %100 ==0:
                        print 'image count of',topic_sub_location,self.image_index[topic_sub_location]
        bag.close()
# Main function.
if __name__ == '__main__':
    # Initialize the node and name it.
    rospy.init_node(PKG,anonymous=True)
    # Go to class functions that do all the heavy lifting. Do error checking.
    try:
        image_creator = ImageCreator()
    except rospy.ROSInterruptException: pass
