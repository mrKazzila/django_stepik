FROM nginx:1.25

RUN \
    apt-get update && \
    apt-get install --no-install-recommends -y \
        openssl && \
    # cleaning cache
    rm -rf /var/cache && \
    rm -rf /var/lib/apt/lists/*

RUN openssl dhparam -out /etc/ssl/dhparam.pem 2048

# Uncomment after generate ssl cert
#RUN rm /etc/nginx/nginx.conf
#COPY nginx.conf /etc/nginx/

RUN rm /etc/nginx/conf.d/default.conf
COPY default.conf /etc/nginx/conf.d/
