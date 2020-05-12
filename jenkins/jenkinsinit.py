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
    if "jenkins" in key:
       print(key)
       break

os.system("kubectl cp ./jenkins/jobs.tar.gz "+key+":/var/jenkins_home/jobs.tar.gz")
os.system("kubectl cp ./jenkins/users.tar.gz "+key+":/var/jenkins_home/users.tar.gz")
os.system("kubectl cp ./jenkins/config.xml "+key+":/var/jenkins_home/config.xml")
os.system("kubectl exec -it "+key+" -- /bin/tar -xzvpf /var/jenkins_home/users.tar.gz -C /var/jenkins_home/")
os.system("kubectl exec -it "+key+" -- /bin/tar -xzvpf /var/jenkins_home/jobs.tar.gz -C /var/jenkins_home/")
os.system("kubectl exec -it "+key+" -- /usr/bin/find /var/jenkins_home -exec touch {} +")
os.system("kubectl exec -it "+key+" -- /usr/bin/wget http://localhost:8080/jnlpJars/jenkins-cli.jar")
#os.system("kubectl exec -it "+key+" -- /usr/local/openjdk-8/bin/java -jar jenkins-cli.jar -auth admin:11ee1c7cb4a9daf80133c23476e2fa3fc0 -s http://localhost:8080 reload-configuration")
os.system("kubectl exec -it "+key+" -- /usr/local/openjdk-8/bin/java -jar jenkins-cli.jar -s http://localhost:8080 reload-configuration")
