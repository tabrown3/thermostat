def update_ac_target_temp(handler, server, sTargetTemp):
    if sTargetTemp != None:
        try:
            server.acTargetTemp = int(sTargetTemp)
        except ValueError:
            print("Input was not a int, try again...")
            handler.send_response(400)
            return
        
    print("AC target temperature: %s" % (server.acTargetTemp))