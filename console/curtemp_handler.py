import requests
CURTEMP_URL = "http://localhost:8080/currenttemp"

def curtemp_handler(args):
    send = args.send
    force = args.force
    reset = args.reset

    if type(send) == int:
        res = requests.post(CURTEMP_URL, params={"curTemp":send})
        print(res.text)
    elif type(force) == int:
        res = requests.post(CURTEMP_URL, params={"curTemp":force, "force":1})
        print(res.text)
    elif reset:
        res = requests.post(CURTEMP_URL, params={"reset":1})
        print(res.text)
    else:
        res = requests.get(CURTEMP_URL)
        print(res.text)