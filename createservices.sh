kubectl create namespace mlflow
kubectl create namespace staging
kubectl create namespace production
kubectl create namespace development
dscacheutil -flushcache
helm init --service-account tiller
helm install hdfs gradiant/hdfs
kubectl create -f https://raw.githubusercontent.com/kubernetes/dashboard/master/aio/deploy/recommended/kubernetes-dashboard.yaml
kubectl create serviceaccount dashboard-admin-sa
kubectl create clusterrolebinding dashboard-admin-sa --clusterrole=cluster-admin --serviceaccount=default:dashboard-admin-sa

kubectl create -f jupyter.yaml 
kubectl create -f tiller-rbac-config.yaml
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v0.46.0/deploy/static/provider/aws/deploy.yaml
 --set controller.extraArgs.enable-ssl-passthrough="true" --set controller.scope.namespace=default --set controller.publishService.enabled=true ingress-nginx/ingress-nginx
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
#helm install docassemble jhpyle/docassemble     --set daHostname=recruit.bayescluster.com --set replicas=1 --set resources.deployment.requests.cpu=1 --set resources.deployment.limits.cpu=2
helm install --wait postgres --values pg-values.yaml bitnami/postgresql --set extendedConfConfigMap=postgresql-config
python3 ./debezium/debeziumcopy.py
python3 ./jenkins/jenkinsinit.py
./mlflow/mlflow.sh
./spark/spark.sh
kubectl create -f jenkins-connector.yaml 
kubectl apply -f rbac-authorization.yml
sleep 1m
python3 updatedns.py
