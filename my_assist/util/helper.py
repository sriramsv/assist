

def get_template(type,userdata):
    data={
    "type":type,
    }
    data.update(userdata)
    headers={"Accept":"application/vnd.api+json","Content-Type": "application/vnd.api+json"}
    return ({"data":data},headers)
