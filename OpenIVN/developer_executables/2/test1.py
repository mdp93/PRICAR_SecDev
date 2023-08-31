from OnlineModeDataStream import OnlineModeDataStream


ds = OnlineModeDataStream()
while True:
	speed = ds.retrieveData("SPEED")
	if speed :
		ds.sendDataOut(speed)
