FROM debian:bullseye-slim

ENV DEBIAN_FRONTEND=noninteractive

# Instalar herramientas de compilación y dependencias
RUN apt-get update && apt-get install -y \
    build-essential \
    bison \
    flex \
    libpam0g-dev \
    libwrap0-dev \
    curl \
    iproute2 \
    iputils-ping \
    nano \
    && rm -rf /var/lib/apt/lists/*

# Descargar y compilar TACACS+ desde fuente oficial (Shrubbery Networks)
WORKDIR /tmp
RUN curl -sL ftp://ftp.shrubbery.net/pub/tac_plus/tacacs-F4.0.4.28.tar.gz -o tacacs.tar.gz || \
    curl -sL https://ftp.gwdg.de/pub/misc/shrubbery/tac_plus/tacacs-F4.0.4.28.tar.gz -o tacacs.tar.gz && \
    tar -xzf tacacs.tar.gz && \
    cd tacacs-F4.0.4.28 && \
    ./configure --prefix=/usr/local && \
    make && \
    make install && \
    cd / && rm -rf /tmp/tacacs*

RUN mkdir -p /etc/tacacs+

COPY tac_plus.conf /etc/tacacs+/tac_plus.conf
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 49

ENTRYPOINT ["/entrypoint.sh"]
