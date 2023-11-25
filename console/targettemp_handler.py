import requests
TARGETTEMP_URL = "http://localhost:8080/targettemp"

def targettemp_handler(args):
    acTemp = args.ac

    if type(acTemp) == int:
        res = requests.post(TARGETTEMP_URL, params={"targetTemp":acTemp, "ac":1})
        print(res.text)
    else:
        res = requests.get(TARGETTEMP_URL)
        print(res.text)