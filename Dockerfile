FROM python:3.7
ADD . ./PiSecurityCamera/
WORKDIR /PiSecurityCamera

EXPOSE 8000 5555
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt
CMD ["python","./Start_Server_temp.py"]