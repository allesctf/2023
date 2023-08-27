FROM ubuntu:latest as builder
WORKDIR /usr/src/app
COPY . .
RUN apt update && apt install -y curl clang pkg-config libssl-dev

RUN curl --proto '=https' --tlsv1.3 https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH /root/.cargo/bin:$PATH
RUN cd implant && cargo build
RUN cp ./implant/target/debug/libimplant.so ./cryptor/src/payload.bin
RUN cd cryptor && cargo run -- unleash_your_power
RUN cp ./cryptor/payload_enc.bin ./injector/src
RUN cd injector && cargo build

FROM ubuntu:latest
RUN set -x && \
    apt-get update && \
    apt-get install -y xinetd dropbear openssh-client sudo && \
    apt-get clean

RUN useradd -d /home/ctf/ -m -s /bin/bash ctf && passwd -d ctf && usermod -aG sudo ctf
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
WORKDIR /home/ctf
COPY run.sh /opt
RUN chmod +x /opt/run.sh
RUN echo "sudo /home/ctf/corrosion &" >> /home/ctf/.bashrc

COPY --from=builder /usr/src/app/injector/target/debug/injector /home/ctf/corrosion

EXPOSE 1024
CMD /opt/run.sh
