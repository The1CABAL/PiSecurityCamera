
@ECHO OFF
docker run -it -p 5000:5000 --name PiCamServer -d PiCamServer

SET check = "docker inspect -f {{.State.Running}} PiCamServer"
IF check == False (
	EXIT
)