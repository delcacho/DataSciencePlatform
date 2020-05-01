from area53 import route53
from boto.route53.exception import DNSServerError
from kubernetes import client, config
from datetime import datetime
import socket
import time

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()

hostnames = {
   "default/ambassador":"api.bayescluster.com",
   "default/ingress-jupyter-nginx-ingress-controller":"ide.bayescluster.com",
   "mlflow/ingress-mlflow-nginx-ingress-controller":"mlflow.bayescluster.com",
   "default/ingress-seldon-nginx-ingress-controller":"grafana.bayescluster.com",
   "default/ingress-superset-nginx-ingress-controller":"superset.bayescluster.com"
}

addresses = {}

v1 = client.CoreV1Api()
print("Listing services with their IPs:")
ret = v1.list_service_for_all_namespaces(watch=False)
for i in ret.items:
    key = "{}/{}".format(i.metadata.namespace, i.metadata.name)
    if i.status.load_balancer.ingress is not None:
       hostname = i.status.load_balancer.ingress[0].hostname
       while True:
          try:
             ip = socket.gethostbyname(hostname)
             break
          except:
             print("Cannot resolve hostname. Retrying in 10 seconds")
             time.sleep(10)
             pass
       print(key)
       if key in hostnames:
          addresses[hostnames[key]] = ip
          print("Service",key,"has IP",ip)

datestr = '"Last update %s."' % datetime.utcnow().strftime('%Y-%m-%d %H:%M')

for i, (k, v) in enumerate(addresses.items()):
   fqdn = k
   dot = k[:k.rfind(".")].rfind(".")
   subdomain = k[0:dot]
   domain = k[dot+1:]
   print(subdomain)
   print(domain)
   zone = route53.get_zone(domain)
   arec = zone.get_a(fqdn)
   try:
      zone.add_a(fqdn, v, 900)
   except:
      zone.update_a(fqdn, v, 900)
   print(arec)
