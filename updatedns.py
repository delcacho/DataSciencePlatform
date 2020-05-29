from area53 import route53
from boto.route53.exception import DNSServerError
from kubernetes import client, config
from datetime import datetime
import socket
import time

def getKeysByValue(dictOfElements, valueToFind):
    listOfKeys = list()
    listOfItems = dictOfElements.items()
    for item  in listOfItems:
        if item[1] == valueToFind:
            listOfKeys.append(item[0])
    return  listOfKeys

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()

hostnames = {
   "api.bayescluster.com":"default/ambassador",
   "ide.bayescluster.com":"default/ingress-https-nginx-ingress-controller",
   "mlflow.bayescluster.com":"default/ingress-mlflow-nginx-ingress-controller",
   "grafana.bayescluster.com":"default/ingress-seldon-nginx-ingress-controller",
   "kibana.bayescluster.com":"default/ingress-kibana-nginx-ingress-controller",
   "superset.bayescluster.com":"default/ingress-http-nginx-ingress-controller",
   "jenkins.bayescluster.com":"default/ingress-http-nginx-ingress-controller",
   "manager.bayescluster.com":"default/ingress-https-nginx-ingress-controller",
   "spark.bayescluster.com":"default/spark-ui-proxy"
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
       if key in hostnames.values():
          hosts = getKeysByValue(hostnames,key)
          for host in hosts:
             addresses[host] = ip
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
