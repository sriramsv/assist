import requests,logging,json

def call_get(url,headers):
    r=requests.get(url,headers=headers)
    if r.status_code!=200:
       return None
    logging.debug(r.json())
    return r.json()

def call_post(url,headers,data):
    r=requests.post(url,headers=headers,data=json.dumps(data))
    if r.status_code!=200:
        return None
    logging.debug(r.json())
    return r.json()



class State(object):
    def __init__(self, d):
        self.__dict__ = d


class Hass():
    def __init__(self,host,port=8123,use_ssl=False,password="password"):
        self.method="https://" if use_ssl else "http://"
        self.port = port
        self.host = host
        self.url = self.method + self.host + ":" + str(self.port)
        self.headers = {'x-ha-access': password,'content-type': 'application/json'}

    def call_service(self,domain,service,service_data={}):
        url=self.url+"/api/services/{}/{}".format(domain,service)
        return call_post(url,self.headers,service_data)


    def fire_event(self,event_name,service_data={}):
        url=self.url+"/api/events/{}".format(event_name)
        return call_post(url,self.headers,service_data)


    def get_state(self,entity_id):
        url=self.url+"/api/states/{}".format(entity_id)
        return State(call_get(url,self.headers))

    def set_event(self,event="test",data={}):
        url=self.url+"/api/event/{}".format(event)
        return call_post(url,self.headers,data)

    @property
    def states(self):
        url=self.url+"/api/states"
        return call_get(url,self.headers)

    @property
    def events(self):
        url=self.url+"/api/events"
        return call_get(url,self.headers)

    @property
    def config(self):
        url=self.url+"/api/config"
        return call_get(url,self.headers)
    @property
    def services(self):
        url=self.url+"/api/services"
        return call_get(url,self.headers)
