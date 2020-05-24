echo "Installing Seldon Core..."
./seldon/s3.sh
kubectl create namespace seldon-system
kubectl create namespace ambassador
kubectl create namespace models

helm install ambassador stable/ambassador --version 1.1.0

helm install seldon-core seldon-core-operator \
    --repo https://storage.googleapis.com/seldon-charts \
    --namespace seldon-system \
    -f ./seldon/values.yaml 

helm install seldon-core-analytics seldon-core-analytics \
   --repo https://storage.googleapis.com/seldon-charts \
   --namespace seldon-system -f ./seldon/grafana.yml

helm install --wait ingress-seldon --set controller.scope.enabled=true \
 --set controller.scope.namespace=seldon-system --set controller.publishService.enabled=true stable/nginx-ingress
kubectl apply -f ./seldon/ingress-seldon.yml
