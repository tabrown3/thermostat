from http.server import BaseHTTPRequestHandler, HTTPServer
import RPi.GPIO as gpio
import urllib
from handle_cur_temp import update_cur_temp
from handle_target_temp import update_ac_target_temp
import json

AC_TARGET_TEMP = 76
AC_THRESHOLD = 2

gpio.setmode(gpio.BCM)
gpio.setup(18, gpio.OUT)
gpio.output(18, gpio.LOW)

hostName = "localhost"
serverPort = 8080

def run_ac_logic(server):
    if server.isCooling and server.curTemp <= server.get_ac_off_temp():
        gpio.output(18, gpio.LOW)
        server.isCooling = False
    elif not server.isCooling and server.curTemp >= server.get_ac_on_temp():
        gpio.output(18, gpio.HIGH)
        server.isCooling = True

class ThermostatServer(HTTPServer):
    isCooling = False
    acTargetTemp = AC_TARGET_TEMP
    acThreshold = AC_THRESHOLD
    curTemp = AC_TARGET_TEMP
    curTempIsForced = False
    def get_ac_on_temp(self):
        return self.acTargetTemp + self.acThreshold
    def get_ac_off_temp(self):
        return self.acTargetTemp - self.acThreshold

class ThermostatRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        splitPath = urllib.parse.urlsplit(self.path)
        parsedPath = splitPath.path
        parsedQuery = urllib.parse.parse_qsl(splitPath.query)

        kv = {}
        for queryArg in parsedQuery:
            queryKey = queryArg[0]
            queryValue = queryArg[1]
            kv[queryKey] = queryValue

        if parsedPath == "/currenttemp":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            curTempParam = kv["curTemp"] if "curTemp" in kv else None
            forceParam = kv["force"] if "force" in kv else None
            resetParam = kv["reset"] if "reset" in kv else None
            update_cur_temp(self, self.server, curTempParam, forceParam, resetParam)
            run_ac_logic(self.server)

            resDict = { "curTemp": self.server.curTemp }
            resJson = json.dumps(resDict)
            self.wfile.write(bytes(resJson, "utf-8"))
        elif parsedPath == "/targettemp":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            targetTempParam = kv["targetTemp"] if "targetTemp" in kv else None
            update_ac_target_temp(self, self.server, targetTempParam)
            run_ac_logic(self.server)

            resDict = { "targetTemp": self.server.acTargetTemp }
            resJson = json.dumps(resDict)
            self.wfile.write(bytes(resJson, "utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        splitPath = urllib.parse.urlsplit(self.path)
        parsedPath = splitPath.path

        if parsedPath == "/currenttemp":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            resDict = { "curTemp": self.server.curTemp }
            resJson = json.dumps(resDict)
            self.wfile.write(bytes(resJson, "utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":        
    webServer = ThermostatServer((hostName, serverPort), ThermostatRequestHandler)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    gpio.cleanup()
    webServer.server_close()
    print("Server stopped.")