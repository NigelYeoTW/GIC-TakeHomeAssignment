FROM node:20-slim AS builder

WORKDIR /app
COPY package*.json ./

ENV NODE_ENV=development
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf.template /etc/nginx/templates/nginx.conf.template

EXPOSE 80

CMD ["/bin/sh", "-c", "envsubst '$VITE_API_URL' < /etc/nginx/templates/nginx.conf.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"]
