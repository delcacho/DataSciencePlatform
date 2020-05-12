from area53 import route53
from boto.route53.exception import DNSServerError
from kubernetes import client, config
from datetime import datetime
import socket
import time
import os

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()

v1 = client.CoreV1Api()
ret = v1.list_pod_for_all_namespaces(watch=False)
for i in ret.items:
    key = i.metadata.name
    if "notebook" in key:
       print(key)
       break

os.system("kubectl cp ./debezium/setup-mlflow-connector.sh "+key+":/home/admin")
os.system("kubectl exec -it "+key+" -- /bin/bash setup-mlflow-connector.sh")
