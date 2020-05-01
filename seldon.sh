./model/s3.sh
kubectl create namespace seldon-system
kubectl create namespace ambassador
kubectl create namespace models

helm install ambassador stable/ambassador --version 1.1.0

helm install seldon-core seldon-core-operator \
    --repo https://storage.googleapis.com/seldon-charts \
    --set usageMetrics.enabled=true \
    --namespace seldon-system \
    --set ambassador.enabled=true 

helm install seldon-core-analytics seldon-core-analytics \
   --repo https://storage.googleapis.com/seldon-charts \
   --namespace seldon-system -f grafana.yml

helm install --wait ingress-seldon --set controller.scope.enabled=true \
 --set controller.scope.namespace=seldon-system --set controller.publishService.enabled=true stable/nginx-ingress
kubectl apply -f ingress-seldon.yml
