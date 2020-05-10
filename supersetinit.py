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
    if "superset" in key:
       print(key)
       break

os.system("kubectl exec -ti "+key+" -- superset-init < superset.txt")
#os.system("kubectl exec -ti "+key+" -- superset import_datasources < datasources.yml")
