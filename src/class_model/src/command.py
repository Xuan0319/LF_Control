#! /usr/bin/env python3
#coding:utf-8

import ssl
import rospy
from std_msgs.msg import String
import paho.mqtt.client as mqtt
import json


 # Ros
def ros_pub(dataJson):
    global publisher, rate ,publisher1 ,publisher2,publisher3,publisher4,publisher5
    # data = json.loads(dataJson)
    publisher.publish(dataJson)     #將date字串發布到topic
    publisher1.publish(dataJson)
    publisher2.publish(dataJson)
    publisher3.publish(dataJson)
    publisher4.publish(dataJson)
    publisher5.publish(dataJson)

    rate.sleep()
    # print(f"publish data {data}")

# MQTT
def on_connect(self, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("cmd/broadcast")


def on_message(self, userdata, msg):
    #msg = msg.payload.decode('utf-8')
    print(f"msg.topic {msg}")
    ros_pub(msg.payload.decode('utf-8'))


def initialise_clients(clientName):
    # callback assignment
    initialise_client = mqtt.Client(clientName, False)
    initialise_client.topic_ack = []
    return initialise_client


if __name__ == '__main__':
    # Mqtt
    mqtt_config = {"host": "140.120.31.133", "port": 1883, "topic": "cmd/broadcast"}
    client = initialise_clients("receiver")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(mqtt_config["host"], mqtt_config["port"], 60)

    # Ros
    Mqtt_Node = 'publisher_py'
    rospy.init_node("cmd_receiver")
    # initialize Ros node
    topicName = 'cmd_receiver'
    publisher = rospy.Publisher(topicName,String,queue_size=10)

    topicName1 = '/drone1/cmd_receiver'
    publisher1 = rospy.Publisher(topicName1,String,queue_size=10)

    topicName2 = '/drone2/cmd_receiver'
    publisher2 = rospy.Publisher(topicName2,String,queue_size=10)

    topicName3 = '/drone3/cmd_receiver'
    publisher3 = rospy.Publisher(topicName3,String,queue_size=10)

    topicName4 = '/drone4/cmd_receiver'
    publisher4 = rospy.Publisher(topicName4,String,queue_size=10)

    topicName5 = '/drone5/cmd_receiver'
    publisher5 = rospy.Publisher(topicName5,String,queue_size=10)


    rate = rospy.Rate(10)

    client.loop_forever()
