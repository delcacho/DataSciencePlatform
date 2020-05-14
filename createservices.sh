kubectl create namespace mlflow
kubectl create namespace staging
kubectl create namespace production
kubectl create namespace none
dscacheutil -flushcache
helm init --service-account tiller
helm install hdfs gradiant/hdfs
kubectl create -f dashboard.yaml
kubectl create -f jupyter.yaml 
kubectl create -f tiller-rbac-config.yaml
helm install --wait ingress-https --set controller.scope.enabled=true \
 --set controller.scope.namespace=default --set controller.publishService.enabled=true stable/nginx-ingress
helm install --wait ingress-http --set controller.scope.enabled=true \
 --set controller.scope.namespace=default --set controller.publishService.enabled=true stable/nginx-ingress
kubectl apply -f ingress-https.yml
kubectl apply -f ingress-http.yml
helm repo add cetic https://cetic.github.io/helm-charts
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add gradiant https://gradiant.github.io/charts
helm repo add kubeless-functions-charts https://kubeless-functions-charts.storage.googleapis.com
helm repo update
./seldon/seldon.sh
./jenkins/jenkins.sh
./debezium/debezium.sh
./superset/superset.sh
helm install --wait postgres --values pg-values.yaml stable/postgresql --set extendedConfConfigMap=postgresql-config
python3 ./debezium/debeziumcopy.py
python3 ./jenkins/jenkinsinit.py
./mlflow/mlflow.sh
./spark/spark.sh
kubectl create -f jenkins-connector.yaml 
kubectl apply -f rbac-authorization.yml
python3 updatedns.py
