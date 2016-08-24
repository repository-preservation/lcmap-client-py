FROM usgseros/ubuntu-gis-py:0.5.0
MAINTAINER USGS LCMAP http://eros.usgs.gov
LABEL Description="This image is used to invoke an iPython REPL for experimenting with the lcmap-client-py project"

RUN curl -O https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py
RUN pip install git+https://github.com/usgs-eros/lcmap-client-py
RUN pip install --upgrade pylru termcolor six requests nose click DateTime numpy
RUN pip install jupyter

ENTRYPOINT ["ipython"]
