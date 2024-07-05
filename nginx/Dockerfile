# Build dist files
FROM node:22.4 AS builder

WORKDIR /frontend
COPY /frontend/package*.json .
RUN npm ci
COPY /frontend .
RUN npm run build

# Build reverse proxy
FROM nginx:1.27

COPY --from=builder /frontend/dist /usr/share/nginx/html
RUN rm /etc/nginx/conf.d/default.conf
COPY /nginx/conf /etc/nginx/conf.d