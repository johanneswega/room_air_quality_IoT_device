import urequests as requests
import keys

# Import your ubidots token from key file
TOKEN = keys.ubidots_token

# Builds the json to send the request
def build_json(variable1, value1, variable2, value2, variable3, value3, variable4, value4):
    try:
        data = {variable1: {"value": value1}, variable2: {"value": value2}, variable3: {"value": value3}, variable4: {"value": value4}}
        return data
    except:
        return None

# Sends the request. Please reference the REST API reference https://ubidots.com/docs/api/
def post_var(device, value1, value2, value3, value4):
    try:
        url = "https://industrial.api.ubidots.com/"
        url = url + "api/v1.6/devices/" + device
        headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

        # Here you can edit the labels
        data = build_json("Temperature", value1, "Humidity", value2, "CO2", value3, "tVOC", value4)
        if data is not None:
            print(data)
            req = requests.post(url=url, headers=headers, json=data)
            return req.json()
        else:
            pass
    except:
        pass
