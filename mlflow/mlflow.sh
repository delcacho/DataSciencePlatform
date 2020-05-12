echo "Installing MLFlow..."
helm repo add larribas https://larribas.me/helm-charts
helm repo update
helm install --wait ingress-mlflow --set controller.scope.enabled=true \
 --set controller.scope.namespace=mlflow --set controller.publishService.enabled=true stable/nginx-ingress
kubectl apply -f ./mlflow/ingress-mlflow.yml
kubectl create secret generic mlflow-postgres --from-literal=password='pruebademlflow'
helm install --wait mlflow --namespace mlflow --values ./mlflow/mlflow-values.yaml larribas/mlflow
