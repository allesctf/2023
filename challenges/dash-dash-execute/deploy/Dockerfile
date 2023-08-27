# docker build -t ddx . && docker run --rm -it -p1024:1024 ddx
# ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ctf@127.0.0.1 -p 1024

# build flagcheck binary with the real flag:
FROM ubuntu@sha256:a02c32cf0c2a7e8743c74deef66637aa70e063c9bd40e9e1f8c0b3ea0750b0ba as builder
RUN apt-get update && apt-get install -y gcc && apt-get clean
COPY flagcheck.c /
ENV FLAG="ALLES!{surprisingly_similar_to_setuid_processes_but_not_actually_secure}"
RUN gcc -DFLAG="\"$FLAG\"" /flagcheck.c -o flagcheck

# setup an SSH host with the flagcheck binary as execute-no-read
FROM ubuntu@sha256:a02c32cf0c2a7e8743c74deef66637aa70e063c9bd40e9e1f8c0b3ea0750b0ba
RUN apt-get update && apt-get install -y gcc dropbear rsync openssh-client && apt-get clean # openssh-client provides scp
COPY --from=builder /flagcheck /usr/bin/flagcheck
RUN chmod -rw /usr/bin/flagcheck
RUN useradd -d /home/ctf/ -m -s /bin/bash ctf && passwd -d ctf
WORKDIR /home/ctf
CMD ["dropbear", "-FBREkwp", "1024"]
