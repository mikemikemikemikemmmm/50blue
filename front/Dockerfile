FROM node:lts-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
RUN find . -mindepth 1 -maxdepth 1 ! -name 'dist' -exec rm -rf {} +