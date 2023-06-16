FROM nginx:1.25

RUN \
    apt-get update && \
    apt-get install --no-install-recommends -y \
        openssl

RUN openssl dhparam -out /etc/ssl/dhparam.pem 2048

# Remove the # after generate ssl cert
#RUN rm /etc/nginx/nginx.conf
#COPY nginx.conf /etc/nginx/

RUN rm /etc/nginx/conf.d/default.conf
COPY default.conf /etc/nginx/conf.d/
