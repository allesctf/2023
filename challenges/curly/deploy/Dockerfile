# docker build -t curly . && docker run --rm -it -p1024:1024 curly
FROM alpine:latest AS builder

RUN set -x && \
    apk add --update alpine-sdk xz && \
    wget -qO /tmp/ynetd.xz https://yx7.cc/code/ynetd/ynetd-0.1.2.tar.xz && \
    tar -xf /tmp/ynetd.xz -C /tmp

RUN apk add --update libcurl curl-dev
COPY curly.c curly.c
RUN set -x && \
    gcc -o /usr/local/bin/curly curly.c -lcurl && \
    make -C /tmp/ynetd-0.1.2 && \
    mv /tmp/ynetd-0.1.2/ynetd /usr/local/bin

RUN echo "int puts(char*); void main(void) {puts(\"ALLES!{might_as_well_add_CURLOPT_RUN_SYSTEM}\"); puts(\"by the way: did you know that curl can 'upload' to file:// URLs ö.Ö\");}" | gcc -o /usr/local/bin/getflag -pipe -x c -

FROM alpine:latest
RUN apk add --update libcurl
COPY --from=builder /usr/local/bin /usr/local/bin
COPY curly.c /
RUN chmod -rw /usr/local/bin/getflag && chmod +s /usr/local/bin/getflag && ln -s /usr/local/bin/getflag /flag
USER guest
EXPOSE 1024
CMD [ "ynetd", "-se", "y", "/usr/local/bin/curly" ]
