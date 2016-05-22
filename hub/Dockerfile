FROM debian:jessie

RUN echo 'sigh'
RUN apt-get update

RUN apt-get install --yes --no-install-recommends \
    python3 \
    python3-pip \
    npm \
    nodejs-legacy \
    git \
    ca-certificates

RUN npm install -g configurable-http-proxy

RUN pip3 install jupyterhub pymysql requests-futures


RUN pip3 install git+https://github.com/yuvipanda/jupyterhub-dummy-authenticator.git@master#egg=dummyauthenticator
RUN pip3 install git+https://github.com/yuvipanda/jupyterhub-kubernetes-spawner.git@master#egg=kubespawner

ADD jupyterhub_config.py /srv/jupyterhub_config.py

WORKDIR /tmp
CMD ["/usr/local/bin/jupyterhub", "--no-ssl", "--config", "/srv/jupyterhub_config.py"]
