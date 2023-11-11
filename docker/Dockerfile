FROM alpine

ARG H_UID=1000
ARG H_GID=1000

RUN apk add --no-cache -X http://dl-cdn.alpinelinux.org/alpine/edge/testing \
      python3 py3-pip libcap libcap2 py3-dnslib

# setup system and user
RUN ln -s /usr/bin/python3 /usr/local/bin/python \
      && addgroup --gid $H_GID user \
      && adduser user --uid $H_UID --ingroup user --gecos "" --home /home/user/ --disabled-password \
      && setcap CAP_NET_BIND_SERVICE=+eip "$(readlink -f /usr/bin/python3)"

# install the code of the repo
RUN python3 -m pip install --no-cache-dir --upgrade pip
COPY ./docker/setup.py /home/user/
RUN pip3 install -e /home/user/

# add source
COPY --chown=user:user ./dns /home/user/dns/
COPY --chown=user:user ./run.py /home/user/

# run
USER user
WORKDIR /home/user/
ENV PYTHONUNBUFFERED=1
EXPOSE 53/udp
CMD ["/usr/bin/python3", "/home/user/run.py"]
