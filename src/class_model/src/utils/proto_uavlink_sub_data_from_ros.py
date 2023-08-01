import orjson
import time
import logging

logger = logging.getLogger("__UAVLINKSUBPUB__")

class Proto_msg_from_ros:
    #Protobuf
    flight_information_msg = None
    #ros
    rate = None
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


    @classmethod
    def callBack_gps(cls, GPS):
        cls.flight_information_msg.gps.LAT = GPS.latitude*10000000
        cls.flight_information_msg.gps.LON = GPS.longitude*10000000
        cls.flight_information_msg.gps.ALT = GPS.altitude
        cls.rate.sleep()


    @classmethod
    def callBack_compass_hdg(cls, Compass):
        cls.flight_information_msg.heading = Compass.data*100
        flightInformationMsg = cls.flight_information_msg.SerializeToString()
        cls.sel.write(cls.f2_code + flightInformationMsg + cls.noEcho_code)
        cls.rate.sleep()


    @classmethod
    def turnOffUavlink(cls):
        time.sleep(0.5)
        cls.sel.write(cls.f1_close_code)
        time.sleep(0.5)
        cls.sel.write(cls.f2_close_code)
