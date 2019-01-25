FROM python:3.6
COPY /root/requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
COPY /root /app
RUN apt-get update
RUN curl https://s3.dualstack.us-east-2.amazonaws.com/aws-xray-assets.us-east-2/xray-daemon/aws-xray-daemon-3.x.rpm -o /app/xray.rpm
RUN apt-get install -y /app/xray.rpm