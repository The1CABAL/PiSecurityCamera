#!/bin/sh
sudo docker run -it -p 8000:8000 -p 5555:5555 --name picamserver -d picamserver && \ 
sleep 5 && \
sudo docker inspect -f {{.State.Running}} picamserver && \
echo "Container is running."