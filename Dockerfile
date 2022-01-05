FROM  python:3.8-slim-buster


RUN apt-get update \
        && apt-get install -y \
        fonts-liberation \
        libappindicator3-1 \
        libatk-bridge2.0-0 \
        libdbus-glib-1-2 \
        curl unzip wget \
        lsb-release \
        libasound2 \
        xdg-utils \
        libnspr4 \
        libnss3 \
        libxss1 \
        libgbm1 \
        xvfb


# install chromedriver and google-chrome
RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    wget https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip -d /usr/bin && \
    chmod +x /usr/bin/chromedriver && \
    rm chromedriver_linux64.zip

RUN CHROME_SETUP=google-chrome.deb && \
    wget -O $CHROME_SETUP "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb" && \
    dpkg -i $CHROME_SETUP && \
    apt install -y -f && \
    rm $CHROME_SETUP


ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONUNBUFFERED=1

ENV APP_HOME /usr/src/app
WORKDIR $APP_HOME

COPY requirements.txt .

RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . $APP_HOME/

CMD ["python3", "main.py"]
