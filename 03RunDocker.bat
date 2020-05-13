
@ECHO OFF
docker run -it -p 8000:8000 --name picamserver -d picamserver

SET check = "docker inspect -f {{.State.Running}} picamserver"
IF check == False (
	EXIT
)