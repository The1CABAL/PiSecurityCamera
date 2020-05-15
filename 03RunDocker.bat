
@ECHO OFF
docker run -it -p 8000:8000 -p 5555:5555 --name picamserver -d picamserver

SET check = "docker inspect -f {{.State.Running}} picamserver"
IF check == False (
	EXIT
)