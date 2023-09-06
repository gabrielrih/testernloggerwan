FROM python:3.11.4-bullseye
WORKDIR /app
COPY requirements/common.txt ./requirements/
RUN pip install --no-cache-dir -r requirements/common.txt
COPY . . 
CMD ["python", "testernlogger.py", "--config=config/config.ini", "--debug"]