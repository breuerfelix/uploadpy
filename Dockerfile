FROM python:3.8-slim-buster

WORKDIR /usr/app

# set timezone
RUN echo "Europe/Berlin" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata

# dependencies for selenium
RUN apt-get install -y --no-install-recommends --no-install-suggests \
  wget bzip2 libgtk-3-0 libdbus-glib-1-2 libx11-xcb1 libxt6 && \
  wget -q -O - "https://download.mozilla.org/?product=firefox-latest-ssl&os=linux64" | tar -xj -C /opt && \
  ln -s /opt/firefox/firefox /usr/local/bin/ && \
  export GECKO_DRIVER_VERSION='v0.29.0' && \
  wget https://github.com/mozilla/geckodriver/releases/download/$GECKO_DRIVER_VERSION/geckodriver-$GECKO_DRIVER_VERSION-linux64.tar.gz && \
  tar -xvzf geckodriver-$GECKO_DRIVER_VERSION-linux64.tar.gz && \
  rm geckodriver-$GECKO_DRIVER_VERSION-linux64.tar.gz && \
  chmod +x geckodriver && \
  cp geckodriver /usr/local/bin/

COPY pyproject.toml .
COPY start.py .
COPY uploadpy uploadpy

# install dependencies for python
RUN pip install .

# otherwhise logs will not get printed to docker logs
ENV PYTHONUNBUFFERED=1

CMD ["python", "start.py"]
