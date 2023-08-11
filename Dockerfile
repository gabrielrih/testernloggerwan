FROM python:3.11.4-bullseye
WORKDIR /home/app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . . 
CMD ["python", "testerNlogger.py", "--config=config/config-example.ini", "--debug"]