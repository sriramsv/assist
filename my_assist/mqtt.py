from threading import Thread
import paho.mqtt.client as mq

class MQTT(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.client=mq.Client(client_id="my_assist")
        self.stop = False

	def run(self):
		while not self.stop and client.loop_forever() == 0:
			pass
		print "MQTT Thread stopped"

    def connect_from_object(self,obj):
        conf=obj()
        self.client.username_pw_set(conf.USERNAME,conf.PASSWORD)
        self.client.subscribe('test',1)
        self.client.onmessage=self.onmessage
        self.client.connect(conf.URL,conf.PORT,1)

    def get_client(self):
        return self.client

    def onmessage(self,client,userdata,message):
        print message.payload
