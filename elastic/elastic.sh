kubectl create namespace logging
helm repo add elastic https://helm.elastic.co
helm install elasticsearch elastic/elasticsearch --version 7.7.0 --namespace logging --set volumeClaimTemplate.resources.requests.storage=10Gi
helm install kibana elastic/kibana --version 7.7.0 --namespace logging --set elasticsearchHosts="http://elasticsearch-master.logging.svc.cluster.local:9200"
helm install fluent-bit stable/fluent-bit --namespace=logging --set backend.type=es --set  backend.es.host="elasticsearch-master.logging.svc.cluster.local" --set filter.mergeJSONLog=true --set extraEntries.filter="Merge_Log_Key logfield" --set backend.es.retry_limit=5
helm install --wait ingress-kibana --set controller.scope.enabled=true \
 --set controller.scope.namespace=logging --set controller.publishService.enabled=true stable/nginx-ingress
kubectl apply -f ./elastic/ingress-kibana.yml
