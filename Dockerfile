FROM python:3.7-alpine
LABEL maintainer="Alexey Miasoedov <alexey.miasoedov@gmail.com>"

ENV PYTHONUNBUFFERED=1
RUN pip install pyroute2
ADD loopbackip.py /usr/local/lib/python3.7/site-packages/
ADD loopback_ip.txt /config/

CMD ["python", "-m", "loopbackip"]
