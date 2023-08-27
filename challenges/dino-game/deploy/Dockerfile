FROM nixos/nix:2.16.0

RUN echo "experimental-features = nix-command flakes" > /etc/nix/nix.conf

RUN mkdir /game
COPY . /game

WORKDIR /game

RUN rm -rf .git && git init && git add .

RUN nix profile install .#env

CMD echo "{\"users\":{\"$TEAM\":\"password123\"},\"freecam\":{}}" > users.json && server --port 1024 --auth_path users.json --clickhouse_url http://click.game.svc.cluster.local:8123
