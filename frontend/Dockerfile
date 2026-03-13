FROM node:20-alpine AS builder

WORKDIR /app
COPY package.json ./

ENV NODE_ENV=development
RUN npm install

COPY . .

ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf.template /etc/nginx/templates/nginx.conf.template

EXPOSE 80

CMD ["/bin/sh", "-c", "envsubst '$VITE_API_URL' < /etc/nginx/templates/nginx.conf.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"]
