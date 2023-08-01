#!/usr/bin/env python3
#coding:utf-8
import paho.mqtt.client as mqtt
import os
import sys
import time
import utils
import proto.flight_information_varint_pb2 as flight_information_varint_pb2
import proto.flyformatioln_pb2 as flyformatioln_pb2
import logging


import rospy
from std_msgs.msg import String
from std_msgs.msg import Float64
from std_msgs.msg import Header
from mavros_msgs.srv import ParamGet
from sensor_msgs.msg import NavSatFix
from sensor_msgs.msg import Imu
from sensor_msgs.msg import Range
from geometry_msgs.msg import Vector3




def init_dataFormat(cfg:utils.Read_PUB_Config):
    if cfg.msg_format == "Proto":
        utils.Proto_msg_from_ros.client = client
        utils.Proto_msg_from_ros.flight_information_msg = flight_information_varint_pb2.flight_information_message()
        utils.Proto_msg_from_ros.flyformatioln_msg = flyformatioln_pb2.fly_formation_message()
        utils.Proto_msg_from_ros.Flight_Information_topicToMqtt = cfg.Flight_Information_topicToMqtt
        utils.Proto_msg_from_ros.Fly_Formation_topicToMqtt = cfg.Fly_Formation_topicToMqtt
        utils.Proto_msg_from_ros.Fly_Formation_topicToMqtt_QOS = cfg.Fly_Formation_topicToMqtt_QOS
        rospy.Subscriber('/mavros/global_position/global', NavSatFix, utils.Proto_msg_from_ros.callBack_gps)
        rospy.Subscriber('/mavros/global_position/compass_hdg', Float64, utils.Proto_msg_from_ros.callBack_compass_hdg)
    elif cfg.msg_format == "Json":
        utils.Json_msg_from_ros.client = client
        utils.Json_msg_from_ros.Flight_Information_topicToMqtt = cfg.Flight_Information_topicToMqtt
        utils.Json_msg_from_ros.Fly_Formation_topicToMqtt = cfg.Fly_Formation_topicToMqtt
        utils.Json_msg_from_ros.Fly_Formation_topicToMqtt_QOS = cfg.Fly_Formation_topicToMqtt_QOS
        rospy.Subscriber('/mavros/global_position/global', NavSatFix, utils.Json_msg_from_ros.callBack_gps)
        rospy.Subscriber('/mavros/global_position/compass_hdg', Float64, utils.Json_msg_from_ros.callBack_compass_hdg)
    else:
        logging.debug("msg_format not found")


def on_connect(self, userdata, flags, rc):
    logger.info("Connected with result code " + str(rc))

def on_publish(self, userdata, mid):
    logger.debug("pub success")

def on_disconnect(client, userdata, rc):
    logger.debug("disconnecting reason  "  +str(rc))
    client.connected_flag=False
    client.disconnect_flag=True

if __name__ == '__main__':
    # Read Config
    FilePath = os.path.join(os.path.dirname(__file__),"utils","mqttConfig_PUB.yml")
    cfg = utils.Read_PUB_Config(FilePath)
    client = utils.MQTTClient(cfg.MQTTClientNamePub)

    # set log
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(log_format)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(cfg.logFileName)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.info(cfg)
    
    # Mqtt
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.connect(host=cfg.host, port=cfg.port, keepalive=cfg.keepalive)
    client.will_set(cfg.willTopic, cfg.lwt, cfg.willTopicQOS, cfg.willRetain)
    client.loop_start()

    # Ros
    rosClient = cfg.ROSClientNamePub
    rospy.init_node(rosClient)
    
    # init data format
    init_dataFormat(cfg)

    try:
        rospy.spin()
    except BaseException as error:
        client.disconnect()
        logger.info("End of program")
        sys.exit()
     
