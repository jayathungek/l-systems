FROM python:3
COPY src/main.py /
COPY src/lsystem.py /
COPY src/graphics/* /graphics/
COPY requirements.txt /

RUN apt-get update && apt-get install -y \
        python-dev python-pip python-setuptools \
        libffi-dev libxml2-dev libxslt1-dev \
        libtiff-dev libjpeg62-turbo-dev zlib1g-dev libfreetype6-dev \
        liblcms2-dev libwebp-dev python-tk

ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt && rm /tmp/requirements.txt


RUN chmod 755 main.py
ENTRYPOINT ["python", "main.py"]
CMD []
