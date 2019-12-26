# Tarea 2 SD
## Integrantes

- Cristian Navarrete
- Benjamin Seider

## General

### Uso
#### Iniciar

    docker-compose up
  
#### Múltiples Clientes 

	docker-compose up --scale client=n

Con n = número de clientes
#### Detener Ejecución
Para pararlo, se debe presionar dos veces ctrl + c (Forzar cierre)

#### Borrar
    docker-compose down
    
## Rutas

#### Logs Servidor

    server/logs.txt

Se ha implementado una simulación de paso de mensajes y listado de usuarios entre los clientes en el caso de que se detecte que es docker

	try:
		text =  input("")
	except  EOFError:


    
## Actividad 1

Se encuentra en la carpeta partea

En este caso no es posible acceder desde afuera de docker al chat (ya que se necesita abrir puertos tanto en el cliente como en el servidor)



## Actividad 2

Se encuentra en la carpeta parteb

También se encuentra implementada una simulación de conversación dentro de docker, pero en este caso si se puede acceder desde fuera de docker si se instalan los paquetes requeridos (requeriments.txt) y se ejecuta de la siguiente forma:

	python client.py 127.0.0.1
 
 127.0.0.1 podría llegar a ser reemplazado por la ip de un servidor remoto en caso de que los puertos esten bien configurados en este (se debe exponer rabbitmq)
