MÉTODO TFTP (RECOMENDADO)

Paso	Comando	Descripción:

    1	IP_ADDRESS=192.168.0.2	Configurar IP del router
    2	IP_SUBNET_MASK=255.255.255.0	Configurar máscara de red
    3	DEFAULT_GATEWAY=192.168.0.1	Configurar gateway
    4	TFTP_SERVER=192.168.0.100	IP del servidor TFTP
    5	TFTP_FILE=c1841-adventerprisek9-mz.124-25f.bin	Nombre exacto del archivo
    6	tftpdnld	Iniciar transferencia
    7	boot flash:archivo.bin	Bootear después de transferir

ftp linux

    sudo apt install tftpd-hpa
    sudo mkdir -p /var/lib/tftpboot
    sudo chmod 777 /var/lib/tftpboot
    sudo systemctl start tftpd-hpa
