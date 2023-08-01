import orjson
import time

class Proto_msg_from_ros:
    #Protobuf
    flight_information_msg = None
    fly_formation_msg = None
    #Mqtt
    client = None
    Flight_Information_topicToMqtt = None
    Fly_Formation_topicToMqtt = None
    Fly_Formation_topicToMqtt_QOS = None

# TODO: gps decimal point fix
    @classmethod
    def callBack_gps(cls, GPS):
        cls.flight_information_msg.LAT = int(GPS.latitude*1e7)
        cls.flight_information_msg.LON = int(GPS.longitude*1e7)
        cls.flight_information_msg.ALT = int(GPS.altitude*1e2)

    @classmethod
    def callBack_compass_hdg(cls, Compass):
        cls.flight_information_msg.heading = int(Compass.data*1e2)
        flightInformationMsg = cls.flight_information_msg.SerializeToString()
        cls.mqtt_Pub(message=flightInformationMsg, topics=cls.Flight_Information_topicToMqtt)
    

    # TODO: Formation.velocity check
    @classmethod
    def callBack_fly_formation(cls, Formation):
        cls.fly_formation_msg.velocity = Formation.velocity
        cls.fly_formation_msg.fly_formation = Formation.type
        flyFormationMsg = cls.fly_formation_msg.SerializeToString()
        cls.mqtt_Pub(message=flyFormationMsg, topics=cls.Fly_Formation_topicToMqtt, qos=cls.Fly_Formation_topicToMqtt_QOS)



    @classmethod
    def mqtt_Pub(cls, message:bytes, topics:str, waitForAck:bool=False, qos:int=0)->None:
        mid = cls.client.publish(topics, message, qos)[1]
        if waitForAck:
            while mid not in cls.client.topic_ack:
                print("wait for ack")
                time.sleep(0.25)
            cls.client.topic_ack.remove(mid)




class Json_msg_from_ros:
    GPS_Data = {}
    Formation_Data = {}
    client = None
    #Mqtt
    Flight_Information_topicToMqtt = None
    Fly_Formation_topicToMqtt = None
    Fly_Formation_topicToMqtt_QOS = None
# TODO: remove str
    @classmethod 
    def callBack_imu(cls, IMU):
        gyro_x=str(IMU.linear_acceleration.x)
        gyro_y=str(IMU.linear_acceleration.y)
        gyro_z=str(IMU.linear_acceleration.z)

        accel_x=str(IMU.angular_velocity.x)
        accel_y=str(IMU.angular_velocity.y)
        accel_z=str(IMU.angular_velocity.z)

        dataImuUpdate = {"gyro_x": gyro_x, "gyro_y": gyro_y,"gyro_z":gyro_z, "accel_x": accel_x, "accel_y": accel_y, "accel_z": accel_z}
        cls.data.update(dataImuUpdate)

    
    @classmethod 
    def callBack_gps(cls, GPS):
        lat=int(GPS.latitude*1e7)   #change the scale to centimeters
        lon=int(GPS.longitude*1e7)
        alt=int(GPS.altitude*1e2)
        dataGpsUpdate = {"lat": lat, "lon": lon, "alt": alt}
        cls.GPS_Data.update(dataGpsUpdate)
        dataJsonFormate = orjson.dumps(cls.GPS_Data)
        cls.mqtt_Pub(message=dataJsonFormate, topics=cls.Flight_Information_topicToMqtt)


# TODO: does decode need utf8 
    @classmethod 
    def callBack_compass_hdg(cls, Compass):
        heading = int(Compass.data*1e2)
        dataGpsUpdate = {"heading": heading}
        cls.GPS_Data.update(dataGpsUpdate)
        dataJsonFormate = orjson.dumps(cls.GPS_Data)
        cls.mqtt_Pub(message=dataJsonFormate, topics=cls.Flight_Information_topicToMqtt)
    @classmethod
    def callBack_fly_formation(cls, Formation):
        Formation_data = {"velocity": Formation.velocity, "type": Formation.type}
        flyFormationMsg = orjson.dumps(Formation_data)
        cls.mqtt_Pub(message=flyFormationMsg, topics=cls.Fly_Formation_topicToMqtt, qos=cls.Fly_Formation_topicToMqtt_QOS)
        
    @classmethod
    def mqtt_Pub(cls, message:str, topics:str, waitForAck:bool=False, qos:int=0):
        mid = cls.client.publish(topics, message, qos)[1]
        if waitForAck:
            while mid not in cls.client.topic_ack:
                print("wait for ack")
                time.sleep(0.25)
            cls.client.topic_ack.remove(mid)
