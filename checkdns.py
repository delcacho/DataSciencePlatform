from area53 import route53
from boto.route53.exception import DNSServerError
from kubernetes import client, config
from datetime import datetime
import socket
import time

# Ensure cluster is running

consec = 0
while consec < 10:
  try:
    ip = socket.gethostbyname("http://api.k8s.dev.bayescluster.com")
    cpnsec += 1
    print("Successful resolution! :)")
  except Exception as e:
    consec = 0
    print(e)
    print("Error in DNS lookup. Gonna sleep for a while...")
    time.sleep(10)
