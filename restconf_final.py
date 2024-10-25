import json
import requests
requests.packages.urllib3.disable_warnings()

# Router IP Address is 10.0.15.181-184
api_url = "https://10.0.15.182/restconf"

# the RESTCONF HTTP headers, including the Accept and Content-Type
# Two YANG data formats (JSON and XML) work with RESTCONF 
headers = {
    "Accept" : "application/yang-data+json", 
    "Content-type" : "application/yang-data+json"
}
basicauth = ("admin", "cisco")

def create():
    yangConfig = {
        "ietf-interfaces:interface" : {
            "name" : "Loopback65070127", 
            "description" : "create loopback", 
            "type": "iana-if-type:softwareLoopback",
            "enabled" : True, 
            "ietf-ip:ipv4" : {
                "address" : [
                    {
                        "ip" : "172.30.127.1", 
                        "netmask" : "255.255.255.0"
                    }
                ]
            },
            "ietf-ip:ipv6" : {}
        }
    }
    resp = requests.put(
        api_url+"/data/ietf-interfaces:interfaces/interface=Loopback65070127",  
        data=json.dumps(yangConfig), 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )
    
    check_resp = requests.get(
        api_url + "/data/ietf-interfaces:interfaces/interface=Loopback65070127",
        auth=basicauth,
        headers=headers,
        verify=False
    )
    
    if check_resp.status_code == 200:
        # ถ้า Interface มีอยู่แล้ว
        print("Cannot create: Interface loopback 65070127")
        return "Cannot create: Interface loopback 65070127"
    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 65070127 is created successfully"
    elif resp.status_code == 409:
        print("Cannot create: Interface loopback 65070127")
        return "Cannot create: Interface loopback 65070127"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Error: Failed to create interface. Status Code: {}".format(resp.status_code)

def delete():
    resp = requests.delete(
        api_url+"/data/ietf-interfaces:interfaces/interface=Loopback65070127",  
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 65070127 is deleted successfully"
    elif resp.status_code == 404:
        # กรณีที่ไม่มี Interface อยู่ (404 Not Found)
        print("Cannot delete: Interface loopback 65070127")
        return "Cannot delete: Interface loopback 65070127"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))


def enable():
    yangConfig = {
        "ietf-interfaces:interface": {
            "name": "Loopback65070127",
            "type": "iana-if-type:softwareLoopback",
            "enabled": True,
        }
    }


    resp = requests.patch(
        api_url+"/data/ietf-interfaces:interfaces/interface=Loopback65070127", 
        data=json.dumps(yangConfig), 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 65070127 is enabled successfully"
    elif resp.status_code == 404:
    # กรณีที่ไม่มี Interface อยู่ (404 Not Found)
        print("Cannot enable: Interface loopback 65070127")
        return "Cannot enable: Interface loopback 65070127"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))


def disable():
    yangConfig = {
        "ietf-interfaces:interface": {
            "name": "Loopback65070127",
            "type": "iana-if-type:softwareLoopback",
            "enabled": False,
        }
    }

    resp = requests.patch(
        api_url+"/data/ietf-interfaces:interfaces/interface=Loopback65070127", 
        data=json.dumps(yangConfig), 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 65070127 is shutdowned successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))


def status():
    api_url_status = "https://10.0.15.182/restconf/data/ietf-interfaces:interfaces-state/interface=Loopback65070127"


    resp = requests.get(
        api_url_status,
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        response_json = resp.json()
        admin_status = response_json["ietf-interfaces:interface"]["admin-status"]
        oper_status = response_json["ietf-interfaces:interface"]["oper-status"]
        if admin_status == 'up' and oper_status == 'up':
            return "Interface loopback65070127 is enabled"
        elif admin_status == 'down' and oper_status == 'down':
            return "Interface loopback65070127 is disabled"
    elif(resp.status_code == 404):
        print("STATUS NOT FOUND: {}".format(resp.status_code))
        return "No Interface loopback 65070127"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
