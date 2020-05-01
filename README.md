# Dask docker images

- Instalar kompose para Mac (instrucciones sobre Linux en https://github.com/kubernetes/kompose)

```
curl -L https://github.com/kubernetes/kompose/releases/download/v1.21.0/kompose-darwin-amd64 -o kompose
chmod +x kompose
sudo mv ./kompose /usr/local/bin/kompose
```

- Construir imagen

```
docker-compose -f docker-compose.yml build
```

- Para instalar librerías, tocar los Dockerfile en los directorios base y notebook

- Levantar cluster local de Kubernetes con:

```
minikube start
```

- Instalar imágenes Docker sobre el cluster local:

```
kompose up
```
# DataSciencePlatform
