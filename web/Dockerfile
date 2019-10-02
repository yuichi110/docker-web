From nginx:1.17.3

COPY ./nginx.conf /etc/nginx/nginx.conf
ADD contents.tar /usr/share/nginx/html

CMD ["nginx", "-g", "daemon off;"]