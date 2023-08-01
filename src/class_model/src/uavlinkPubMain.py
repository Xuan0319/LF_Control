#!/usr/bin/env python3
#coding:utf-8
import serial
import time
import sys
import os
import proto.flight_information_pb2 as flight_information_pb2
import logging
from utils.readConfig import Config
from utils.proto_uavlink_sub_data_from_ros import Proto_msg_from_ros

import rospy
from std_msgs.msg import String
from std_msgs.msg import Float64
from std_msgs.msg import Header
from mavros_msgs.srv import ParamGet
from sensor_msgs.msg import NavSatFix
from sensor_msgs.msg import Imu
from sensor_msgs.msg import Range
from geometry_msgs.msg import Vector3


class Read_UAVLINK_PUB_Config(Config):
    def setAttribute(self):
        super().setAttribute()

    def __init__(self, inFileName):      
        super().__init__(inFileName)
        self.sectionNames = ["UAVLINK","ROS","LOG"]
        self.options = {
            self.sectionNames[0]:{
                            "uavlink_msg_format": (str,False),
                            "uav_id": (str,False),
                            "baudrate": (int,True),
                            "ttyport": (str,True)},
            self.sectionNames[1]:{
                            "ROSClientNamePub": (str,True),
                            "ROStopicName_Flight_Information": (str,False)},
            self.sectionNames[2]:{
                            "logFileName":(str,True)}}
        self.setAttribute()



def init_dataFormat(cfg):
    Proto_msg_from_ros.sel = serial.Serial(cfg.ttyport, cfg.baudrate, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)
    Proto_msg_from_ros.flight_information_msg = flight_information_pb2.flight_information_message()
    Proto_msg_from_ros.rate = rospy.Rate(10)
    rospy.Subscriber('/mavros/global_position/global', NavSatFix, Proto_msg_from_ros.callBack_gps)
    rospy.Subscriber('/mavros/global_position/compass_hdg', Float64, Proto_msg_from_ros.callBack_compass_hdg)

def shutdown_callback():
    Proto_msg_from_ros.turnOffUavlink()
if __name__ == '__main__':
    FilePath = os.path.join(os.path.dirname(__file__),"utils","uavlinkConfig_PUB.yml")
    cfg = Read_UAVLINK_PUB_Config(FilePath)
    print(cfg)
    # set log
    stream_log_format = "%(asctime)s - %(levelname)s - %(message)s"
    file_log_format = "%(message)s"
    file_formatter = logging.Formatter(file_log_format)
    stream_formatter = logging.Formatter(stream_log_format)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(stream_formatter)
    stream_handler.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(cfg.logFileName, mode='w')
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.INFO)

    logger = logging.getLogger("__UAVLINKSUBPUB__")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.debug(cfg)

    # Ros
    rosClient = cfg.ROSClientNamePub
    rospy.init_node(rosClient)
    rospy.on_shutdown(shutdown_callback)
    # init data format
    init_dataFormat(cfg)

    try:
        rospy.spin()
    except KeyboardInterrupt as e:
        Proto_msg_from_ros.turnOffUavlink()
        logger.debug("End of program")
        sys.exit()

     




