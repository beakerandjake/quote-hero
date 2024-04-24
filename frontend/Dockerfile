FROM node:21-alpine as build

WORKDIR /app

COPY package.json package.json
COPY package-lock.json package-lock.json
RUN npm ci

COPY public ./public
COPY vite.config.js tailwind.config.js postcss.config.js index.html  .
COPY src ./src
RUN npm run build


FROM nginx:1.25.3-alpine-slim
COPY --from=build /app/dist /usr/share/nginx/html