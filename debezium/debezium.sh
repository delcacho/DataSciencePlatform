echo "Installing Debezium..."
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add incubator https://kubernetes-charts-incubator.storage.googleapis.com
helm repo update
helm install --wait kafka bitnami/kafka --set external.enabled=false
kubectl create -f ./debezium/kafka-client-deploy.yaml
kubectl wait pod/kafka-client --for condition=ready
kubectl exec kafka-client -- kafka-topics --zookeeper kafka-zookeeper:2181 --topic connect-offsets --create --partitions 1 --replication-factor 1 --config "cleanup.policy=compact"
kubectl exec kafka-client -- kafka-topics --zookeeper kafka-zookeeper:2181 --topic connect-configs --create --partitions 1 --replication-factor 1 --config "cleanup.policy=compact"
kubectl exec kafka-client -- kafka-topics --zookeeper kafka-zookeeper:2181 --topic connect-status --create --partitions 1 --replication-factor 1 --config "cleanup.policy=compact"
kubectl create -f ./debezium/kafka-connect-deploy.yaml
kubectl wait service/kafkaconnect-service --for condition=ready
kubectl create configmap --from-file=./debezium/extended.conf postgresql-config
