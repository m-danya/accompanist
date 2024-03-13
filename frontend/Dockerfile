FROM node:20 as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install -g @vue/cli && npm install
COPY . .
ARG NGINX_PORT
ENV VUE_APP_BACKEND_PORT=$NGINX_PORT
RUN npm run build

FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]