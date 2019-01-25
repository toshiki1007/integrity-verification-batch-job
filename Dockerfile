FROM python:3.6
COPY /root/requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
COPY /root /app
ENTRYPOINT ["python", "/app/bin/batch_job.py"]