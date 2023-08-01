#!/usr/bin/env python3
#coding:utf-8
import serial
import time
import sys
import os
import proto.flight_information_pb2 as flight_information_pb2
import logging
from utils.readConfig import Config
from utils.proto_uavlink_pub_data_to_ros import Proto_msg_to_ros
import google.protobuf.message

import rospy
from std_msgs.msg import String
from std_msgs.msg import Float64
from std_msgs.msg import Header
from mavros_msgs.srv import ParamGet
from sensor_msgs.msg import NavSatFix
from sensor_msgs.msg import Imu
from sensor_msgs.msg import Range
from geometry_msgs.msg import Vector3
# costom msg
from class_model.msg import FlightInformation


class Read_UAVLINK_SUB_Config(Config):
    def setAttribute(self):
        super().setAttribute()

    def __init__(self, inFileName):      
        super().__init__(inFileName)
        self.sectionNames = ["UAVLINK","ROS","LOG"]
        self.options = {
            self.sectionNames[0]:{
                            "uavlink_msg_format": (str,False),
                            "uav_id": (str,False),
                            "baudrate": (int,False),
                            "ttyport": (str,True)},
            self.sectionNames[1]:{
                            "ROSClientNameSub": (str,True),
                            "ROStopicName_Flight_Information": (str,True)},
            self.sectionNames[2]:{
                            "logFileName":(str,False)}}
        self.setAttribute()


def init_dataFormat(cfg):
    Proto_msg_to_ros.flight_information_msg = flight_information_pb2.flight_information_message()
    Proto_msg_to_ros.rate = rospy.Rate(10)
    Proto_msg_to_ros.publisher_Flight_Information = rospy.Publisher(cfg.ROStopicName_Flight_Information,FlightInformation,queue_size=10)
    Proto_msg_to_ros.FlightInformationRosMsg = FlightInformation()
    Proto_msg_to_ros.sel = sel

def shutdown_callback():
    Proto_msg_to_ros.turnOffUavlink()

if __name__ == '__main__':
    FilePath = os.path.join(os.path.dirname(__file__),"utils","uavlinkConfig_SUB.yml")
    cfg = Read_UAVLINK_SUB_Config(FilePath)
    
    sel = serial.Serial(cfg.ttyport, cfg.baudrate, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)
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

    logger = logging.getLogger("__UAVLINKSUB__")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.debug(cfg)

    rospy.init_node(cfg.ROSClientNameSub)  
    rospy.on_shutdown(shutdown_callback)
    init_dataFormat(cfg)

    while not rospy.is_shutdown():
        try:
            if sel.in_waiting >= 25:
                readTenByte = sel.read_until(expected= b'\x01\x17', size=25)        
                Proto_msg_to_ros.on_message_Flight_Information(readTenByte)

        except google.protobuf.message.DecodeError as e:
            logger.info("DecodeError:{}".format(e))
            logger.info("readTenByte:{}".format(readTenByte))
        except rospy.ROSInterruptException as e:
            Proto_msg_to_ros.turnOffUavlink()
            print("End of program")
            sys.exit()




