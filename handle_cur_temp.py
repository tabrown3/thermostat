def update_cur_temp(handler, server, sCurTemp, sForce, sReset):
    if sForce != None:
        server.curTempIsForced = True
    
    if sReset != None:
        server.curTempIsForced = False

    if sCurTemp != None:
        try:
            # if the curTemp has been forced, future updates must be forced
            if (server.curTempIsForced and sForce != None) or not server.curTempIsForced:
                server.curTemp = int(sCurTemp)
        except ValueError:
            print("Input was not a int, try again...")
            handler.send_response(400)
            return

    print("Current temperature: %s" % (server.curTemp))
    print("Current force state: %s" % (server.curTempIsForced))