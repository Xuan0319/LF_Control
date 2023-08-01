import time

import proto.flight_information_pb2 as flight_information_pb2
import google.protobuf.json_format as json_format
import logging
# costom msg


# TODO: use native ros type instead of json or str
logger = logging.getLogger("__SUB__")

class Proto_msg_to_ros:
    #Protobuf
    flight_information_msg = None

    #Ros publisher
    FlightInformationRosMsg = None
    rate = None
    publisher_Flight_Information = None

    #uavlink 
    sel = None
    payload = b"......................"
    noEcho_code = b"\x0d\x0a"
    echo_code = b"\x0d\x1a"
    close_code = b"\x0d\x2a"
    f1_code = b"\xf1"
    f2_code = b"\xf2"
    f1_close_code = f1_code + payload + close_code
    f2_close_code = f2_code + payload + close_code

    #Proto
    @classmethod
    def on_message_Flight_Information(cls, msg):
        cls.publisher_Flight_Information.publish(cls.convert_proto_to_ros(msg[1:-2]))
        cls.rate.sleep()
    
    @classmethod
    def convert_proto_to_ros(cls, proto):
        proto_msg = cls.flight_information_msg.FromString(proto)
        cls.FlightInformationRosMsg.LAT = proto_msg.gps.LAT
        cls.FlightInformationRosMsg.LON = proto_msg.gps.LON
        cls.FlightInformationRosMsg.ALT = proto_msg.gps.ALT
        cls.FlightInformationRosMsg.heading = proto_msg.heading
        return cls.FlightInformationRosMsg
    
    @classmethod
    def detection(cls):
        cls.sel.write(cls.f1_code + cls.payload + cls.echo_code)

    @classmethod
    def turnOffUavlink(cls):
        time.sleep(0.5)
        cls.sel.write(cls.f1_close_code)
        time.sleep(0.5)
        cls.sel.write(cls.f2_close_code)    
