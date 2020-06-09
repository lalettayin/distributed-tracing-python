FROM python:3.8-alpine

COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt
COPY . /app 

ENTRYPOINT ["python", "/app/addition.py"]
