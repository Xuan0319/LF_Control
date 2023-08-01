import orjson
import time

import logging

# TODO: use native ros type instead of json or str
logger = logging.getLogger("__CMD__")

class Proto_msg_to_ros:
    pass

class Json_msg_to_ros:
    rate = None
    # Ros publisher
    publisher_Cmd_Broadcast = None
    
    Cmd_Broadcast_topicToMqtt = None


    @classmethod
    def ros_pub(cls, dataJson):
        if dataJson.topic == cls.Cmd_Broadcast_topicToMqtt:
            logger.debug(dataJson.payload.decode("UTF-8"))
            cls.publisher_Cmd_Broadcast.publish(dataJson.payload.decode("UTF-8"))
            cls.rate.sleep()
        else:
            logger.info("topic not found")
            

    @staticmethod
    def on_message(client, userdata, msg):
        Json_msg_to_ros.ros_pub(msg)