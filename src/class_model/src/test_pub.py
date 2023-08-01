#!/usr/bin/env python3
#coding:utf-8
import rospy
# from mavros_msgs.msg import Waypoint
from diagnostic_msgs.msg import KeyValue
 
def callBack(data):
    print (data)

 
if __name__ == '__main__':
    nodeName = 'subscriber_py'
    rospy.init_node(nodeName)
    topicName = '/Flight_Information_reciver'
    subscriber = rospy.Subscriber(topicName,KeyValue,callBack)  #從topic獲取string再呼叫callback
    rospy.spin()