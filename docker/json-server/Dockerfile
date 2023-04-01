FROM node:19-alpine3.16

RUN npm install -g json-server
COPY ./tests/fixtures/db.json ./db.json
EXPOSE 3000
