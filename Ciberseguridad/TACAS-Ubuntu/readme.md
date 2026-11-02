annotations:
  - type: text
    border_color: '#00000000'
    border_style: ''
    color: '#1F2937'
    rotation: 0
    text_bold: true
    text_content: |-
      🔐 LAB SSH + TACACS+
      Dominio: lab.local | SSHv2 en todos los equipos
      Usuario local: admin / Admin123
      Enable: cisco123
      TACACS+: 10.10.10.2 | key: demo
      Ruteo: OSPF área 0 | NAT en RT-EDGE
    text_font: monospace
    text_italic: false
    text_size: 11
    text_unit: pt
    thickness: 1
    x1: -760.0
    y1: -480.0
    z_index: 1
  - type: text
    border_color: '#00000000'
    border_style: ''
    color: '#B91C1C'
    rotation: 0
    text_bold: false
    text_content: |-
      RT-EDGE
      Gi0/0: DHCP (NAT / Internet)
      Gi0/1: 10.0.0.1/30  → RT-1
      Gi0/2: 10.0.0.5/30  → RT-2
      Gi0/3: 10.0.0.9/30  → RT-3
      Gi0/4: 10.0.0.13/30 → RT-4
      Gi0/5: 10.10.10.1/24 → TACACS
    text_font: monospace
    text_italic: false
    text_size: 10
    text_unit: pt
    thickness: 1
    x1: -360.0
    y1: -330.0
    z_index: 1
  - type: text
    border_color: '#00000000'
    border_style: ''
    color: '#047857'
    rotation: 0
    text_bold: false
    text_content: |-
      TACACS-SRV (Ubuntu)
      ens2: 10.10.10.2/24
      GW: 10.10.10.1
      TCP 49 (tac_plus-ng)
      SSH: cisco / cisco
    text_font: monospace
    text_italic: false
    text_size: 10
    text_unit: pt
    thickness: 1
    x1: 380.0
    y1: -300.0
    z_index: 1
  - type: text
    border_color: '#00000000'
    border_style: ''
    color: '#1D4ED8'
    rotation: 0
    text_bold: false
    text_content: |-
      RT-1
      Gi0/0: 10.0.0.2/30
      Gi0/1.10: 192.168.10.1/24
    text_font: monospace
    text_italic: false
    text_size: 10
    text_unit: pt
    thickness: 1
    x1: -440.0
    y1: -80.0
    z_index: 1
  - type: text
    border_color: '#00000000'
    border_style: ''
    color: '#1D4ED8'
    rotation: 0
    text_bold: false
    text_content: |-
      RT-2
      Gi0/0: 10.0.0.6/30
      Gi0/1.20: 192.168.20.1/24
    text_font: monospace
    text_italic: false
    text_size: 10
    text_unit: pt
    thickness: 1
    x1: -120.0
    y1: -80.0
    z_index: 1
  - type: text
    border_color: '#00000000'
    border_style: ''
    color: '#1D4ED8'
    rotation: 0
    text_bold: false
    text_content: |-
      RT-3
      Gi0/0: 10.0.0.10/30
      Gi0/1.30: 192.168.30.1/24
    text_font: monospace
    text_italic: false
    text_size: 10
    text_unit: pt
    thickness: 1
    x1: 200.0
    y1: -80.0
    z_index: 1
  - type: text
    border_color: '#00000000'
    border_style: ''
    color: '#1D4ED8'
    rotation: 0
    text_bold: false
    text_content: |-
      RT-4
      Gi0/0: 10.0.0.14/30
      Gi0/1.40: 192.168.40.1/24
    text_font: monospace
    text_italic: false
    text_size: 10
    text_unit: pt
    thickness: 1
    x1: 520.0
    y1: -80.0
    z_index: 1
  - type: text
    border_color: '#00000000'
    border_style: ''
    color: '#7C3AED'
    rotation: 0
    text_bold: false
    text_content: |-
      SW-1 · VLAN 10
      SVI: 192.168.10.2/24
      GW: 192.168.10.1
      Gi0/0 trunk | Gi0/1-3 access
    text_font: monospace
    text_italic: false
    text_size: 10
    text_unit: pt
    thickness: 1
    x1: -560.0
    y1: 210.0
    z_index: 1
  - type: text
    border_color: '#00000000'
    border_style: ''
    color: '#7C3AED'
    rotation: 0
    text_bold: false
    text_content: |-
      SW-2 · VLAN 20
      SVI: 192.168.20.2/24
      GW: 192.168.20.1
      Gi0/0 trunk | Gi0/1-3 access
    text_font: monospace
    text_italic: false
    text_size: 10
    text_unit: pt
    thickness: 1
    x1: -240.0
    y1: 210.0
    z_index: 1
  - type: text
    border_color: '#00000000'
    border_style: ''
    color: '#7C3AED'
    rotation: 0
    text_bold: false
    text_content: |-
      SW-3 · VLAN 30
      SVI: 192.168.30.2/24
      GW: 192.168.30.1
      Gi0/0 trunk | Gi0/1-3 access
    text_font: monospace
    text_italic: false
    text_size: 10
    text_unit: pt
    thickness: 1
    x1: 80.0
    y1: 210.0
    z_index: 1
  - type: text
    border_color: '#00000000'
    border_style: ''
    color: '#7C3AED'
    rotation: 0
    text_bold: false
    text_content: |-
      SW-4 · VLAN 40
      SVI: 192.168.40.2/24
      GW: 192.168.40.1
      Gi0/0 trunk | Gi0/1-3 access
    text_font: monospace
    text_italic: false
    text_size: 10
    text_unit: pt
    thickness: 1
    x1: 400.0
    y1: 210.0
    z_index: 1
nodes:
  - boot_disk_size: null
    configuration: NAT
    cpu_limit: null
    cpus: null
    data_volume: null
    hide_links: false
    id: n0
    image_definition: null
    label: INTERNET
    node_definition: external_connector
    ram: null
    tags: []
    x: 0
    y: -440
    interfaces:
      - id: i0
        label: port
        slot: 0
        type: physical
  - boot_disk_size: null
    configuration: |-
      hostname RT-EDGE
      no ip domain-lookup
      ip domain-name lab.local
      enable secret cisco123
      username admin privilege 15 secret Admin123
      !
      aaa new-model
      aaa authentication login TACACS_LOGIN group tacacs+ local
      aaa authentication login CONSOLE none
      !
      tacacs server TACACS-SERVER
       address ipv4 10.10.10.2
       key demo
       timeout 3
      !
      crypto key generate rsa general-keys modulus 2048
      ip ssh version 2
      ip ssh time-out 60
      ip ssh authentication-retries 3
      !
      interface GigabitEthernet0/0
       description WAN-NAT
       ip address dhcp
       ip nat outside
       no shutdown
      !
      interface GigabitEthernet0/1
       description TO-RT-1
       ip address 10.0.0.1 255.255.255.252
       ip nat inside
       no shutdown
      !
      interface GigabitEthernet0/2
       description TO-RT-2
       ip address 10.0.0.5 255.255.255.252
       ip nat inside
       no shutdown
      !
      interface GigabitEthernet0/3
       description TO-RT-3
       ip address 10.0.0.9 255.255.255.252
       ip nat inside
       no shutdown
      !
      interface GigabitEthernet0/4
       description TO-RT-4
       ip address 10.0.0.13 255.255.255.252
       ip nat inside
       no shutdown
      !
      interface GigabitEthernet0/5
       description TO-TACACS-SRV
       ip address 10.10.10.1 255.255.255.0
       ip nat inside
       no shutdown
      !
      router ospf 1
       router-id 1.1.1.1
       passive-interface GigabitEthernet0/5
       network 10.0.0.0 0.0.0.15 area 0
       network 10.10.10.0 0.0.0.255 area 0
       default-information originate
      !
      ip access-list standard NAT-INSIDE
       permit 10.0.0.0 0.255.255.255
       permit 192.168.0.0 0.0.255.255
      !
      ip nat inside source list NAT-INSIDE interface GigabitEthernet0/0 overload
      !
      line con 0
       login authentication CONSOLE
       exec-timeout 0 0
       logging synchronous
      line vty 0 4
       login authentication TACACS_LOGIN
       transport input ssh
       exec-timeout 5 0
      !
      end
    cpu_limit: null
    cpus: null
    data_volume: null
    hide_links: false
    id: n1
    image_definition: null
    label: RT-EDGE
    node_definition: iosv
    ram: null
    tags: []
    x: 0
    y: -240
    interfaces:
      - id: i0
        label: GigabitEthernet0/0
        slot: 0
        type: physical
      - id: i1
        label: GigabitEthernet0/1
        slot: 1
        type: physical
      - id: i2
        label: GigabitEthernet0/2
        slot: 2
        type: physical
      - id: i3
        label: GigabitEthernet0/3
        slot: 3
        type: physical
      - id: i4
        label: GigabitEthernet0/4
        slot: 4
        type: physical
      - id: i5
        label: GigabitEthernet0/5
        slot: 5
        type: physical
  - boot_disk_size: null
    configuration: |-
      #cloud-config
      hostname: TACACS-SRV
      manage_etc_hosts: true
      system_info:
        default_user:
          name: cisco
      password: cisco
      chpasswd: { expire: false }
      ssh_pwauth: true
      write_files:
        - path: /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg
          content: |
            network: {config: disabled}
        - path: /etc/netplan/99-lab.yaml
          permissions: '0600'
          content: |
            network:
              version: 2
              ethernets:
                lan:
                  match:
                    name: "ens*"
                  dhcp4: false
                  addresses: [10.10.10.2/24]
                  routes:
                    - to: default
                      via: 10.10.10.1
                  nameservers:
                    addresses: [8.8.8.8, 1.1.1.1]
      runcmd:
        - rm -f /etc/netplan/50-cloud-init.yaml
        - netplan apply
    cpu_limit: null
    cpus: null
    data_volume: null
    hide_links: false
    id: n2
    image_definition: null
    label: TACACS-SRV
    node_definition: ubuntu
    ram: null
    tags: []
    x: 320
    y: -240
    interfaces:
      - id: i0
        label: ens2
        slot: 0
        type: physical
  - boot_disk_size: null
    configuration: |-
      hostname RT-1
      no ip domain-lookup
      ip domain-name lab.local
      enable secret cisco123
      username admin privilege 15 secret Admin123
      !
      aaa new-model
      aaa authentication login TACACS_LOGIN group tacacs+ local
      aaa authentication login CONSOLE none
      !
      tacacs server TACACS-SERVER
       address ipv4 10.10.10.2
       key demo
       timeout 3
      !
      crypto key generate rsa general-keys modulus 2048
      ip ssh version 2
      ip ssh time-out 60
      ip ssh authentication-retries 3
      !
      interface GigabitEthernet0/0
       description TO-RT-EDGE
       ip address 10.0.0.2 255.255.255.252
       no shutdown
      !
      interface GigabitEthernet0/1
       description TRUNK-TO-SW-1
       no ip address
       no shutdown
      !
      interface GigabitEthernet0/1.10
       description VLAN10
       encapsulation dot1Q 10
       ip address 192.168.10.1 255.255.255.0
      !
      router ospf 1
       router-id 2.2.2.2
       passive-interface GigabitEthernet0/1.10
       network 10.0.0.0 0.0.0.3 area 0
       network 192.168.10.0 0.0.0.255 area 0
      !
      line con 0
       login authentication CONSOLE
       exec-timeout 0 0
       logging synchronous
      line vty 0 4
       login authentication TACACS_LOGIN
       transport input ssh
       exec-timeout 5 0
      !
      end
    cpu_limit: null
    cpus: null
    data_volume: null
    hide_links: false
    id: n3
    image_definition: null
    label: RT-1
    node_definition: iosv
    ram: null
    tags: []
    x: -480
    y: -40
    interfaces:
      - id: i0
        label: GigabitEthernet0/0
        slot: 0
        type: physical
      - id: i1
        label: GigabitEthernet0/1
        slot: 1
        type: physical
  - boot_disk_size: null
    configuration: |-
      hostname RT-2
      no ip domain-lookup
      ip domain-name lab.local
      enable secret cisco123
      username admin privilege 15 secret Admin123
      !
      aaa new-model
      aaa authentication login TACACS_LOGIN group tacacs+ local
      aaa authentication login CONSOLE none
      !
      tacacs server TACACS-SERVER
       address ipv4 10.10.10.2
       key demo
       timeout 3
      !
      crypto key generate rsa general-keys modulus 2048
      ip ssh version 2
      ip ssh time-out 60
      ip ssh authentication-retries 3
      !
      interface GigabitEthernet0/0
       description TO-RT-EDGE
       ip address 10.0.0.6 255.255.255.252
       no shutdown
      !
      interface GigabitEthernet0/1
       description TRUNK-TO-SW-2
       no ip address
       no shutdown
      !
      interface GigabitEthernet0/1.20
       description VLAN20
       encapsulation dot1Q 20
       ip address 192.168.20.1 255.255.255.0
      !
      router ospf 1
       router-id 3.3.3.3
       passive-interface GigabitEthernet0/1.20
       network 10.0.0.4 0.0.0.3 area 0
       network 192.168.20.0 0.0.0.255 area 0
      !
      line con 0
       login authentication CONSOLE
       exec-timeout 0 0
       logging synchronous
      line vty 0 4
       login authentication TACACS_LOGIN
       transport input ssh
       exec-timeout 5 0
      !
      end
    cpu_limit: null
    cpus: null
    data_volume: null
    hide_links: false
    id: n4
    image_definition: null
    label: RT-2
    node_definition: iosv
    ram: null
    tags: []
    x: -160
    y: -40
    interfaces:
      - id: i0
        label: GigabitEthernet0/0
        slot: 0
        type: physical
      - id: i1
        label: GigabitEthernet0/1
        slot: 1
        type: physical
  - boot_disk_size: null
    configuration: |-
      hostname RT-3
      no ip domain-lookup
      ip domain-name lab.local
      enable secret cisco123
      username admin privilege 15 secret Admin123
      !
      aaa new-model
      aaa authentication login TACACS_LOGIN group tacacs+ local
      aaa authentication login CONSOLE none
      !
      tacacs server TACACS-SERVER
       address ipv4 10.10.10.2
       key demo
       timeout 3
      !
      crypto key generate rsa general-keys modulus 2048
      ip ssh version 2
      ip ssh time-out 60
      ip ssh authentication-retries 3
      !
      interface GigabitEthernet0/0
       description TO-RT-EDGE
       ip address 10.0.0.10 255.255.255.252
       no shutdown
      !
      interface GigabitEthernet0/1
       description TRUNK-TO-SW-3
       no ip address
       no shutdown
      !
      interface GigabitEthernet0/1.30
       description VLAN30
       encapsulation dot1Q 30
       ip address 192.168.30.1 255.255.255.0
      !
      router ospf 1
       router-id 4.4.4.4
       passive-interface GigabitEthernet0/1.30
       network 10.0.0.8 0.0.0.3 area 0
       network 192.168.30.0 0.0.0.255 area 0
      !
      line con 0
       login authentication CONSOLE
       exec-timeout 0 0
       logging synchronous
      line vty 0 4
       login authentication TACACS_LOGIN
       transport input ssh
       exec-timeout 5 0
      !
      end
    cpu_limit: null
    cpus: null
    data_volume: null
    hide_links: false
    id: n5
    image_definition: null
    label: RT-3
    node_definition: iosv
    ram: null
    tags: []
    x: 160
    y: -40
    interfaces:
      - id: i0
        label: GigabitEthernet0/0
        slot: 0
        type: physical
      - id: i1
        label: GigabitEthernet0/1
        slot: 1
        type: physical
  - boot_disk_size: null
    configuration: |-
      hostname RT-4
      no ip domain-lookup
      ip domain-name lab.local
      enable secret cisco123
      username admin privilege 15 secret Admin123
      !
      aaa new-model
      aaa authentication login TACACS_LOGIN group tacacs+ local
      aaa authentication login CONSOLE none
      !
      tacacs server TACACS-SERVER
       address ipv4 10.10.10.2
       key demo
       timeout 3
      !
      crypto key generate rsa general-keys modulus 2048
      ip ssh version 2
      ip ssh time-out 60
      ip ssh authentication-retries 3
      !
      interface GigabitEthernet0/0
       description TO-RT-EDGE
       ip address 10.0.0.14 255.255.255.252
       no shutdown
      !
      interface GigabitEthernet0/1
       description TRUNK-TO-SW-4
       no ip address
       no shutdown
      !
      interface GigabitEthernet0/1.40
       description VLAN40
       encapsulation dot1Q 40
       ip address 192.168.40.1 255.255.255.0
      !
      router ospf 1
       router-id 5.5.5.5
       passive-interface GigabitEthernet0/1.40
       network 10.0.0.12 0.0.0.3 area 0
       network 192.168.40.0 0.0.0.255 area 0
      !
      line con 0
       login authentication CONSOLE
       exec-timeout 0 0
       logging synchronous
      line vty 0 4
       login authentication TACACS_LOGIN
       transport input ssh
       exec-timeout 5 0
      !
      end
    cpu_limit: null
    cpus: null
    data_volume: null
    hide_links: false
    id: n6
    image_definition: null
    label: RT-4
    node_definition: iosv
    ram: null
    tags: []
    x: 480
    y: -40
    interfaces:
      - id: i0
        label: GigabitEthernet0/0
        slot: 0
        type: physical
      - id: i1
        label: GigabitEthernet0/1
        slot: 1
        type: physical
  - boot_disk_size: null
    configuration: |-
      hostname SW-1
      no ip domain-lookup
      ip domain-name lab.local
      enable secret cisco123
      username admin privilege 15 secret Admin123
      !
      aaa new-model
      aaa authentication login TACACS_LOGIN group tacacs+ local
      aaa authentication login CONSOLE none
      !
      tacacs server TACACS-SERVER
       address ipv4 10.10.10.2
       key demo
       timeout 3
      !
      crypto key generate rsa general-keys modulus 2048
      ip ssh version 2
      ip ssh time-out 60
      ip ssh authentication-retries 3
      !
      vlan 10
       name VLAN10
      !
      interface GigabitEthernet0/0
       description TRUNK-TO-RT-1
       switchport trunk encapsulation dot1q
       switchport mode trunk
       switchport trunk allowed vlan 10
       no shutdown
      !
      interface range GigabitEthernet0/1 - 3
       switchport mode access
       switchport access vlan 10
       spanning-tree portfast
       no shutdown
      !
      interface Vlan1
       shutdown
      !
      interface Vlan10
       ip address 192.168.10.2 255.255.255.0
       no shutdown
      !
      no ip routing
      ip default-gateway 192.168.10.1
      !
      line con 0
       login authentication CONSOLE
       exec-timeout 0 0
       logging synchronous
      line vty 0 15
       login authentication TACACS_LOGIN
       transport input ssh
       exec-timeout 5 0
      !
      end
    cpu_limit: null
    cpus: null
    data_volume: null
    hide_links: false
    id: n7
    image_definition: null
    label: SW-1
    node_definition: iosvl2
    ram: null
    tags: []
    x: -480
    y: 160
    interfaces:
      - id: i0
        label: GigabitEthernet0/0
        slot: 0
        type: physical
      - id: i1
        label: GigabitEthernet0/1
        slot: 1
        type: physical
      - id: i2
        label: GigabitEthernet0/2
        slot: 2
        type: physical
      - id: i3
        label: GigabitEthernet0/3
        slot: 3
        type: physical
  - boot_disk_size: null
    configuration: |-
      hostname SW-2
      no ip domain-lookup
      ip domain-name lab.local
      enable secret cisco123
      username admin privilege 15 secret Admin123
      !
      aaa new-model
      aaa authentication login TACACS_LOGIN group tacacs+ local
      aaa authentication login CONSOLE none
      !
      tacacs server TACACS-SERVER
       address ipv4 10.10.10.2
       key demo
       timeout 3
      !
      crypto key generate rsa general-keys modulus 2048
      ip ssh version 2
      ip ssh time-out 60
      ip ssh authentication-retries 3
      !
      vlan 20
       name VLAN20
      !
      interface GigabitEthernet0/0
       description TRUNK-TO-RT-2
       switchport trunk encapsulation dot1q
       switchport mode trunk
       switchport trunk allowed vlan 20
       no shutdown
      !
      interface range GigabitEthernet0/1 - 3
       switchport mode access
       switchport access vlan 20
       spanning-tree portfast
       no shutdown
      !
      interface Vlan1
       shutdown
      !
      interface Vlan20
       ip address 192.168.20.2 255.255.255.0
       no shutdown
      !
      no ip routing
      ip default-gateway 192.168.20.1
      !
      line con 0
       login authentication CONSOLE
       exec-timeout 0 0
       logging synchronous
      line vty 0 15
       login authentication TACACS_LOGIN
       transport input ssh
       exec-timeout 5 0
      !
      end
    cpu_limit: null
    cpus: null
    data_volume: null
    hide_links: false
    id: n8
    image_definition: null
    label: SW-2
    node_definition: iosvl2
    ram: null
    tags: []
    x: -160
    y: 160
    interfaces:
      - id: i0
        label: GigabitEthernet0/0
        slot: 0
        type: physical
      - id: i1
        label: GigabitEthernet0/1
        slot: 1
        type: physical
      - id: i2
        label: GigabitEthernet0/2
        slot: 2
        type: physical
      - id: i3
        label: GigabitEthernet0/3
        slot: 3
        type: physical
  - boot_disk_size: null
    configuration: |-
      hostname SW-3
      no ip domain-lookup
      ip domain-name lab.local
      enable secret cisco123
      username admin privilege 15 secret Admin123
      !
      aaa new-model
      aaa authentication login TACACS_LOGIN group tacacs+ local
      aaa authentication login CONSOLE none
      !
      tacacs server TACACS-SERVER
       address ipv4 10.10.10.2
       key demo
       timeout 3
      !
      crypto key generate rsa general-keys modulus 2048
      ip ssh version 2
      ip ssh time-out 60
      ip ssh authentication-retries 3
      !
      vlan 30
       name VLAN30
      !
      interface GigabitEthernet0/0
       description TRUNK-TO-RT-3
       switchport trunk encapsulation dot1q
       switchport mode trunk
       switchport trunk allowed vlan 30
       no shutdown
      !
      interface range GigabitEthernet0/1 - 3
       switchport mode access
       switchport access vlan 30
       spanning-tree portfast
       no shutdown
      !
      interface Vlan1
       shutdown
      !
      interface Vlan30
       ip address 192.168.30.2 255.255.255.0
       no shutdown
      !
      no ip routing
      ip default-gateway 192.168.30.1
      !
      line con 0
       login authentication CONSOLE
       exec-timeout 0 0
       logging synchronous
      line vty 0 15
       login authentication TACACS_LOGIN
       transport input ssh
       exec-timeout 5 0
      !
      end
    cpu_limit: null
    cpus: null
    data_volume: null
    hide_links: false
    id: n9
    image_definition: null
    label: SW-3
    node_definition: iosvl2
    ram: null
    tags: []
    x: 160
    y: 160
    interfaces:
      - id: i0
        label: GigabitEthernet0/0
        slot: 0
        type: physical
      - id: i1
        label: GigabitEthernet0/1
        slot: 1
        type: physical
      - id: i2
        label: GigabitEthernet0/2
        slot: 2
        type: physical
      - id: i3
        label: GigabitEthernet0/3
        slot: 3
        type: physical
  - boot_disk_size: null
    configuration: |-
      hostname SW-4
      no ip domain-lookup
      ip domain-name lab.local
      enable secret cisco123
      username admin privilege 15 secret Admin123
      !
      aaa new-model
      aaa authentication login TACACS_LOGIN group tacacs+ local
      aaa authentication login CONSOLE none
      !
      tacacs server TACACS-SERVER
       address ipv4 10.10.10.2
       key demo
       timeout 3
      !
      crypto key generate rsa general-keys modulus 2048
      ip ssh version 2
      ip ssh time-out 60
      ip ssh authentication-retries 3
      !
      vlan 40
       name VLAN40
      !
      interface GigabitEthernet0/0
       description TRUNK-TO-RT-4
       switchport trunk encapsulation dot1q
       switchport mode trunk
       switchport trunk allowed vlan 40
       no shutdown
      !
      interface range GigabitEthernet0/1 - 3
       switchport mode access
       switchport access vlan 40
       spanning-tree portfast
       no shutdown
      !
      interface Vlan1
       shutdown
      !
      interface Vlan40
       ip address 192.168.40.2 255.255.255.0
       no shutdown
      !
      no ip routing
      ip default-gateway 192.168.40.1
      !
      line con 0
       login authentication CONSOLE
       exec-timeout 0 0
       logging synchronous
      line vty 0 15
       login authentication TACACS_LOGIN
       transport input ssh
       exec-timeout 5 0
      !
      end
    cpu_limit: null
    cpus: null
    data_volume: null
    hide_links: false
    id: n10
    image_definition: null
    label: SW-4
    node_definition: iosvl2
    ram: null
    tags: []
    x: 480
    y: 160
    interfaces:
      - id: i0
        label: GigabitEthernet0/0
        slot: 0
        type: physical
      - id: i1
        label: GigabitEthernet0/1
        slot: 1
        type: physical
      - id: i2
        label: GigabitEthernet0/2
        slot: 2
        type: physical
      - id: i3
        label: GigabitEthernet0/3
        slot: 3
        type: physical
links:
  - id: l0
    n1: n0
    n2: n1
    i1: i0
    i2: i0
    label: INTERNET-port<->RT-EDGE-Gi0/0
  - id: l1
    n1: n1
    n2: n3
    i1: i1
    i2: i0
    label: RT-EDGE-Gi0/1<->RT-1-Gi0/0
  - id: l2
    n1: n1
    n2: n4
    i1: i2
    i2: i0
    label: RT-EDGE-Gi0/2<->RT-2-Gi0/0
  - id: l3
    n1: n1
    n2: n5
    i1: i3
    i2: i0
    label: RT-EDGE-Gi0/3<->RT-3-Gi0/0
  - id: l4
    n1: n1
    n2: n6
    i1: i4
    i2: i0
    label: RT-EDGE-Gi0/4<->RT-4-Gi0/0
  - id: l5
    n1: n1
    n2: n2
    i1: i5
    i2: i0
    label: RT-EDGE-Gi0/5<->TACACS-SRV-ens2
  - id: l6
    n1: n3
    n2: n7
    i1: i1
    i2: i0
    label: RT-1-Gi0/1<->SW-1-Gi0/0
  - id: l7
    n1: n4
    n2: n8
    i1: i1
    i2: i0
    label: RT-2-Gi0/1<->SW-2-Gi0/0
  - id: l8
    n1: n5
    n2: n9
    i1: i1
    i2: i0
    label: RT-3-Gi0/1<->SW-3-Gi0/0
  - id: l9
    n1: n6
    n2: n10
    i1: i1
    i2: i0
    label: RT-4-Gi0/1<->SW-4-Gi0/0
lab:
  description: RT-EDGE con NAT a Internet, 4 routers de acceso con router-on-a-stick, 4 switches con una VLAN cada uno, SSHv2 y AAA TACACS+ con fallback local.
  notes: |-
    Credenciales: admin / Admin123 | enable: cisco123 | Ubuntu: cisco / cisco
    TACACS+: 10.10.10.2, key demo (instalar tac_plus-ng manualmente según la guía)
    Mientras TACACS+ no esté operativo, SSH entra con el usuario local por fallback.
  title: Lab SSH + TACACS+ (4 VLAN)
  version: 0.2.2
