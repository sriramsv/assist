import requests,logging,json,jsontree

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






class Hass():
    def __init__(self,host,port=8123,use_ssl=False,password="password"):
        self.method="https://" if use_ssl else "http://"
        self.port = port
        self.host = host
        self.url = self.method + self.host + ":" + str(self.port)+"/api"
        self.headers = {'x-ha-access': password,'content-type': 'application/json'}
        entitieslist=self.services
        self.serviceaction={}
        for e in entitieslist:
            domain=e['domain']
            service=Service(e)
            self.serviceaction[domain]=service

    def call_service(self,domain,service,service_data={}):
        url=self.url+"/services/{}/{}".format(domain,service)
        return call_post(url,self.headers,service_data)

    def get_services_for_entity(self,entity,switch):
        d=entity.split(".")[0]
        try:
            return d+"/"+self.serviceaction[d].get_services(switch)[0]
        except KeyError:
            return None

    def fire_event(self,event_name,service_data={}):
        url=self.url+"/events/{}".format(event_name)
        return call_post(url,self.headers,service_data)


    def get_state(self,entity_id):
        url=self.url+"/states/{}".format(entity_id)
        return jsontree.jsontree(call_get(url,self.headers))

    def set_event(self,event="test",data={}):
        url=self.url+"/event/{}".format(event)
        return call_post(url,self.headers,data)

    @property
    def states(self):
        url=self.url+"/states"
        return call_get(url,self.headers)

    @property
    def events(self):
        url=self.url+"/events"
        return call_get(url,self.headers)

    @property
    def config(self):
        url=self.url+"/config"
        return call_get(url,self.headers)

    @property
    def services(self):
        url=self.url+"/services"
        return call_get(url,self.headers)

class Service():
    def __init__(self,data):
        self.d=jsontree.jsontree(data)

    def get_services(self,switch):
        return filter(lambda s: switch in s, self.d.services.keys())
