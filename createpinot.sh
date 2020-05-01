kubectl create -f tiller-rbac-config.yaml
helm init --wait --service-account tiller
helm repo add stable https://kubernetes-charts.storage.googleapis.com/
helm repo update
helm install ingress --wait stable/nginx-ingress
helm install \
  my-presto \
  --values values.yaml \
  https://github.com/wiwdata/presto-chart/raw/master/charts/presto-1.tgz
helm install superset --wait stable/superset
