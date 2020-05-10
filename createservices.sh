kubectl create namespace mlflow
dscacheutil -flushcache
helm init --service-account tiller
helm install hdfs gradiant/hdfs
kubectl create -f dashboard.yaml
kubectl create -f jupyter.yaml 
#kubectl create -f enterprise-gateway.yaml
#kubectl -n kubernetes-dashboard describe secret $(kubectl -n kubernetes-dashboard get secret | grep admin-user | awk '{print $1}')
kubectl create -f tiller-rbac-config.yaml
helm install --wait ingress-https --set controller.scope.enabled=true \
 --set controller.scope.namespace=default --set controller.publishService.enabled=true stable/nginx-ingress
helm install --wait ingress-http --set controller.scope.enabled=true \
 --set controller.scope.namespace=default --set controller.publishService.enabled=true stable/nginx-ingress
helm install --wait ingress-mlflow --set controller.scope.enabled=true \
 --set controller.scope.namespace=mlflow --set controller.publishService.enabled=true stable/nginx-ingress
kubectl apply -f ingress-https.yml
kubectl apply -f ingress-http.yml
kubectl apply -f ingress-mlflow.yml
kubectl apply -f sparkproxy.yaml
helm repo add cetic https://cetic.github.io/helm-charts
helm repo add larribas https://larribas.me/helm-charts
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add gradiant https://gradiant.github.io/charts
helm repo update
./seldon.sh
kubectl apply -f jenkins/jenkins-secrets.yaml
kubectl apply -f jenkins/jenkins-credentials.yaml
helm install jenkins stable/jenkins -f jenkins/jenkins-values.yaml
helm install superset stable/superset
helm install --wait postgres --values pg-values.yaml bitnami/postgresql
helm install --wait spark bitnami/spark --set worker.replicaCount=4
#helm install --name spark stable/spark
kubectl create secret generic mlflow-postgres --from-literal=password='pruebademlflow' 
helm install --wait mlflow --namespace mlflow --values mlflow-values.yaml larribas/mlflow
kubectl apply -f rbac-authorization.yml
python3 supersetinit.py
python3 updatedns.py
