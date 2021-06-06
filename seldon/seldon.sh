echo "Installing Seldon Core..."
./seldon/s3.sh
kubectl create namespace seldon-system
kubectl create namespace ambassador
helm repo add datawire https://www.getambassador.io
helm repo update
helm install ambassador --namespace ambassador datawire/ambassador

helm install seldon-core seldon-core-operator \
    --repo https://storage.googleapis.com/seldon-charts \
    --namespace seldon-system \
    -f ./seldon/values.yaml 

helm install seldon-core-analytics seldon-core-analytics \
   --repo https://storage.googleapis.com/seldon-charts \
   --namespace seldon-system -f ./seldon/grafana.yml

kubectl apply -f ./seldon/ingress-seldon.yml
