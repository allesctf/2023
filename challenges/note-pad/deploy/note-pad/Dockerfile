FROM node:12.11.0-alpine

WORKDIR /app

COPY package.json yarn.lock ./

RUN yarn  --no-progress --frozen-lockfile install

ADD . /app/

RUN yarn build

USER node
EXPOSE 3000


CMD sh -c 'REACT_APP_API_ROOT=https://${SESSIONID}-1024-note-pad.${CHALLENGE_DOMAIN}:31337 node server/server.js'