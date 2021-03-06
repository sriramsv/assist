
import os
from datetime import timedelta


def get_template(type,userdata):
    data={
    "type":type,
    }
    data.update(userdata)
    headers={"Accept":"application/vnd.api+json","Content-Type": "application/vnd.api+json"}
    return ({"data":data},headers)

def get_base_url():
    port = os.getenv("PORT")
    return "http://0.0.0.0:"+port


def calc_delay(delay):
    s=timedelta(**delay)
    return s.seconds
