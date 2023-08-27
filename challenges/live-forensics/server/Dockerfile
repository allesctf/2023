FROM rust:latest
WORKDIR /usr/app
COPY c2_server .
RUN cargo build --release
CMD ./target/release/c2_server
