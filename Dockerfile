FROM amazonlinux
RUN amazon-linux-extras install python3
RUN yum install -y gcc python3-devel
COPY /root/requirements.txt /requirements.txt
RUN yum localinstall -y  http://dev.mysql.com/get/mysql57-community-release-el7-7.noarch.rpm
RUN yum install -y mysql-community-devel
RUN pip3 install --upgrade setuptools
RUN pip3 install -r /requirements.txt
COPY /root /app
RUN yum install -y unzip
RUN curl -o daemon.zip https://s3.dualstack.us-east-2.amazonaws.com/aws-xray-assets.us-east-2/xray-daemon/aws-xray-daemon-linux-3.x.zip
RUN unzip daemon.zip && cp xray /usr/bin/xray
ENTRYPOINT ["/usr/bin/xray", "-b", "0.0.0.0:2000"]
EXPOSE 2000/udp