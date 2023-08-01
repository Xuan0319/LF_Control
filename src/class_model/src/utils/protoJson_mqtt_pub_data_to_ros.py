import orjson
import time

import proto.flight_information_pb2 as flight_information_pb2
import proto.flyformatioln_pb2 as flyformatioln_pb2
import google.protobuf.json_format as json_format

class Proto_msg_to_ros:
    #Protobuf
    flight_information_msg = None
    fly_formation_msg = None # delcare in function 

    #Ros publisher
    rate = None
    publisher_Flight_Information = None
    publisher_Fly_Formation = None
    #Ros msg
    FlightInformationRosMsg = None

    #Mqtt topic: check data from which topic
    Flight_Information_topicToMqtt = None
    Fly_Formation_topicToMqtt = None

    @classmethod
    def on_message_Flight_Information(cls, client, userdata, msg):
        cls.publisher_Flight_Information.publish(cls.convert_proto_to_ros(msg.payload))
        cls.rate.sleep()


    #TODO: still json format, not change to ros msg yet
    @classmethod
    def on_message_Fly_Formation(cls, client, userdata, msg):
        proto_msg = cls.fly_formation_msg.FromString(msg.payload)
        # protoTOJson_msg = json_format.MessageToJson(proto_msg, indent=None, preserving_proto_field_name=True)
        protoTOJson_msg = json_format.MessageToJson(proto_msg, indent=None, preserving_proto_field_name=True, use_integers_for_enums=True)
        cls.publisher_Fly_Formation.publish(protoTOJson_msg)
        cls.rate.sleep()
       
    # @classmethod
    # def ros_pub(cls, dataProto):
    #     if dataProto.topic == cls.Flight_Information_topicToMqtt:
    #         cls.publisher_Flight_Information.publish(cls.convert_proto_to_ros(dataProto.payload))
    #         cls.rate.sleep()
    #     elif dataProto.topic == cls.Fly_Formation_topicToMqtt:
            
    #         proto_msg = cls.fly_formation_msg.FromString(dataProto.payload)
    #         # protoTOJson_msg = json_format.MessageToJson(proto_msg, indent=None, preserving_proto_field_name=True)
    #         protoTOJson_msg = json_format.MessageToJson(proto_msg, indent=None, preserving_proto_field_name=True, use_integers_for_enums=True)
    #         cls.publisher_Fly_Formation.publish(protoTOJson_msg)
    #         cls.rate.sleep()
    #     else:
    #         print("topic not found")

    @classmethod
    def convert_proto_to_ros(cls, proto):
        proto_msg = cls.flight_information_msg.FromString(proto)
        cls.FlightInformationRosMsg.LAT = proto_msg.LAT
        cls.FlightInformationRosMsg.LON = proto_msg.LON
        cls.FlightInformationRosMsg.ALT = proto_msg.ALT
        cls.FlightInformationRosMsg.heading = proto_msg.heading
        return cls.FlightInformationRosMsg  




class Json_msg_to_ros:
    rate = None
    #Ros publisher
    publisher_Flight_Information = None
    publisher_Fly_Formation = None
    #Ros msg
    FlightInformationRosMsg = None 
    #Mqtt topic: check data from which topic
    Flight_Information_topicToMqtt = None
    Fly_Formation_topicToMqtt = None


    @classmethod
    def on_message_Fly_Formation(cls, client, userdata, msg):
        cls.publisher_Fly_Formation.publish(msg.payload.decode("UTF-8"))
        cls.rate.sleep()

    @classmethod
    def on_message_Flight_Information(cls, client, userdata, msg):
        cls.publisher_Flight_Information.publish(cls.convert_proto_to_ros(msg.payload.decode("UTF-8")))
        cls.rate.sleep()
    # @classmethod
    # def ros_pub(cls, dataJson):
    #     if dataJson.topic == cls.Flight_Information_topicToMqtt:
    #         cls.publisher_Flight_Information.publish(cls.convert_proto_to_ros(dataJson.payload.decode("UTF-8")))
    #         cls.rate.sleep()
    #     elif dataJson.topic == cls.Fly_Formation_topicToMqtt:
    #         cls.publisher_Fly_Formation.publish(dataJson.payload.decode("UTF-8"))
    #         cls.rate.sleep()
    #     else:
    #         print("topic not found")
            
    @classmethod
    def convert_proto_to_ros(cls, json):
        FlightDict = orjson.loads(json)
        cls.FlightInformationRosMsg.LAT = FlightDict.get("lat")
        cls.FlightInformationRosMsg.LON = FlightDict.get("lon")
        cls.FlightInformationRosMsg.ALT = FlightDict.get("alt")
        cls.FlightInformationRosMsg.heading = FlightDict.get("heading")
        return cls.FlightInformationRosMsg

    # @staticmethod
    # def on_message(client, userdata, msg):
    #     Json_msg_to_ros.ros_pub(msg)

