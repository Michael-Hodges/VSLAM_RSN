## VSLAM_RSN
# Data Extraction from bag
To extract pictures from the rosbag perform the following:
cd to catkin_workspace and run catkin_make
source devel/setup.bash

rosrun imagesfrombag getimagesfrombag.py <rosbag file>

Will automatically create folder in same location as the rosbag
