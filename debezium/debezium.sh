echo "Installing Debezium..."
helm repo add incubator https://kubernetes-charts-incubator.storage.googleapis.com
helm repo update
helm install --wait kafka incubator/kafka --set external.enabled=true
kubectl create -f ./debezium/kafka-client-deploy.yaml
kubectl wait pod/kafka-client --for condition=available
kubectl exec kafka-client -- kafka-topics --zookeeper kafka-zookeeper:2181 --topic connect-offsets --create --partitions 1 --replication-factor 1
kubectl exec kafka-client -- kafka-topics --zookeeper kafka-zookeeper:2181 --topic connect-configs --create --partitions 1 --replication-factor 1
kubectl exec kafka-client -- kafka-topics --zookeeper kafka-zookeeper:2181 --topic connect-status --create --partitions 1 --replication-factor 1
kubectl create -f ./debezium/kafka-connect-deploy.yaml
kubectl wait service/kafkaconnect-service --for condition=available
kubectl create configmap --from-file=./debezium/extended.conf postgresql-config
