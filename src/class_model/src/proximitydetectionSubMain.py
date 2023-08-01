#!/usr/bin/env python3
#coding:utf-8
import serial
import time
import sys
import os
import proto.flight_information_pb2 as flight_information_pb2
import logging
from utils.readConfig import Read_SUB_Config
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


def init_dataFormat(cfg:Read_SUB_Config):
    Proto_msg_to_ros.flight_information_msg = flight_information_pb2.flight_information_message()
    Proto_msg_to_ros.rate = rospy.Rate(10)
    Proto_msg_to_ros.publisher_Flight_Information = rospy.Publisher(cfg.Dron550_ROStopicName_Flight_Information,FlightInformation,queue_size=10)
    Proto_msg_to_ros.FlightInformationRosMsg = FlightInformation()
    Proto_msg_to_ros.sel = sel
    Proto_msg_to_ros.detection()

    
if __name__ == '__main__':
    FilePath = os.path.join(os.path.dirname(__file__),"utils","uavlinkConfig_SUB.yml")
    cfg = Read_SUB_Config(FilePath)
    
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
    init_dataFormat(cfg)
 


    while True:
        try:
            logger.debug(sel.read_until(size=25))
            # if sel.in_waiting >= 25:
            #     readTenByte = sel.read_until(expected= b'\x01\x17', size=25)        
            #     Proto_msg_to_ros.on_message_Flight_Information(readTenByte)

        except google.protobuf.message.DecodeError as e:
            logger.info("DecodeError:{}".format(e))
            logger.info("readTenByte:{}".format(readTenByte))
        except KeyboardInterrupt as e:
            Proto_msg_to_ros.turnOffUavlink()
            print("End of program")
            sys.exit()




