# Recuperación de Equipos Cisco

## Routers Cisco (1841) - TFTP

    IP_ADDRESS=192.168.0.2
    IP_SUBNET_MASK=255.255.255.0
    DEFAULT_GATEWAY=192.168.0.1
    TFTP_SERVER=192.168.0.100
    TFTP_FILE=c1841-adventerprisek9-mz.124-25f.bin
    tftpdnld
    boot flash:archivo.bin

Configuración Servidor TFTP Ubuntu

    sudo apt install tftpd-hpa
    sudo mkdir -p /var/lib/tftpboot
    sudo chmod 777 /var/lib/tftpboot
    sudo systemctl start tftpd-hpa
    sudo cp archivo.bin /var/lib/tftpboot/
