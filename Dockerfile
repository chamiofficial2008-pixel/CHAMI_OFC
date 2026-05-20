FROM node:20-slim

RUN apt-get update && apt-get install -y ffmpeg python3 python3-pip

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .

CMD ["node", "index.js"]
