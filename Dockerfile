FROM python:3.7
WORKDIR ./

EXPOSE 8000
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt
CMD ["python","PiSecurityCamera/Start_Server.py"]