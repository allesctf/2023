# docker build -t seebeesee . && docker run --rm -it -p1024:1024 seebeesee
FROM pypy:3

ENV DEBIAN_FRONTEND=noninteractive 
RUN apt-get update && apt-get install -y xinetd socat && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/

# Install dependencies
RUN pip install --no-cache-dir --progress-bar=off pycryptodome

# challenge files
COPY flag /
COPY seebeesee.py /opt/seebeesee.py
#COPY python_svc /etc/xinetd.d/

#ENV TERM=linux TERMINFO=/etc/terminfo
RUN chmod +x /opt/seebeesee.py
EXPOSE 1024

ENTRYPOINT [ "socat", "tcp-l:1024,reuseaddr,fork", "exec:'/opt/seebeesee.py'" ]
