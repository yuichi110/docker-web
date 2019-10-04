From nginx:1.17.3

COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./docroot/index.html /usr/share/nginx/html
RUN mkdir /usr/share/nginx/html/static
COPY ./docroot/static /usr/share/nginx/html/static

CMD ["nginx", "-g", "daemon off;"]