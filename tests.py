import requests
import json,simplejson

# url = 'http://127.0.0.1:5000/api/statereminder'
# headers = {'Accept': 'application/vnd.api+json'}
#
# filters = [dict(name='state', op='eq', val='Work')]
# params = {'filter[objects]': json.dumps(filters)}
#
# response = requests.get(url, params=params, headers=headers)
# assert response.status_code == 200
# print(response.json())



def patch_test():
    data = {
    "type": "statereminder",
    "id": "8",
    "attributes": {
        "event": "Exit"
    }
}
    url = "http://localhost:5000/api/statereminder/8"
    headers={"Accept":"application/vnd.api+json","Content-Type": "application/vnd.api+json"}
    resp = requests.patch(url, simplejson.dumps({"data": data}), headers=headers)
    print resp.status_code,resp.text

patch_test()
