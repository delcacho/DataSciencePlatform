kubectl apply -f ./spark/sparkproxy.yaml
helm install --wait spark bitnami/spark --set worker.replicaCount=4