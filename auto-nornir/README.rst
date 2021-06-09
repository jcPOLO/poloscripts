# Para el entorno de test es necesario poder llegar desde la maquina hasta el EVE-NG
todo esto es para acordarme yo, poco uso para ti tiene este readme

Uso el lab FW VPN ASA prueba.unl

Tengo que levantar los cacharros:

- Sustituto_A10
- Sustituto_Firewall
- R1
- R2
- R3
- R11 (coreswitch)

A los dos que tengo acceso son Sustituto_A10 y R1.
Para llegar, tengo que meter rutas estaticas hasta los cacharros en la maquina
que apunten al EVE-NG

En windows:

- route add 198.18.18.49 mask 255.255.255.255 192.168.1.90
- route add 198.18.18.10 mask 255.255.255.255 192.168.1.90

En linux:

- route add -host 198.18.18.49 gw 192.168.1.90
- route add -host 198.18.18.10 gw 192.168.1.90

Siendo 198.18.18.49 el R1, la .10 el A10 y 192.168.1.90 la IP del EVE-NG

En la parte de EVE-NG tengo levantado un cloud sirviendo DHCP en la red:

198.18.18.0/24

R1 natea todas las redes internas del lab a su pata en la 198.18.18.49 para dar acceso a internet (overload)
