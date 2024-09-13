# Guía de inicio rápido: Compose y Django por Mario Medina

Esta guía de inicio rápido demuestra cómo usar Docker Compose para configurar y ejecutar una aplicación simple de Django REST framework. Antes de empezar,
[instala Compose](https://docs.docker.com/compose/install/).

### Software utilizado

```
Django==4.1.5
django-cors-headers==3.13.0
djangorestframework==3.14.0
djangorestframework-simplejwt==5.2.2
```


## Deploy con docker compose

```
$ docker compose up -d
```

## Resultados esperados

La lista de contenedores debe mostrar un contenedor en ejecución y la asignación de puertos como se muestra a continuación:
```
$ docker ps
CONTAINER ID   IMAGE                      COMMAND                  CREATED          STATUS          PORTS                    NAMES
592d45a62886   django001-backend_django   "python manage.py ru…"   27 seconds ago   Up 25 seconds   0.0.0.0:8000->8000/tcp   backend_django

```

Después de que se inicie la aplicación, vaya a `http://localhost:8000` en su navegador web:


