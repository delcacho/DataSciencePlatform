from kafka import KafkaConsumer
import json
import requests
import logging
from urllib.parse import quote

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

consumer = KafkaConsumer(
   'postgres.public.model_versions',
   bootstrap_servers=['kafka:9092'],
   value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

token = "gundisalvo"
user = "admin"
password = "11ee1c7cb4a9daf80133c23476e2fa3fc0"
session = requests.Session()
session.auth = (user, password)

for message in consumer:
    message = message.value
    payload = message["payload"]
    after = payload["after"]
    operation = payload["op"]
    if operation in ["c","u"]:
       name = after["name"]
       version = after["version"]
       stage = after["current_stage"]
       source = after["source"]
       logging.info("Going to launch Jenkins job: name={}, version={}, stage={}, source={}".format(name,version,stage,source))
       url = "http://jenkins:8080/job/SeldonDeployer/buildWithParameters?token={}"\
          "&name={}&version={}&stage={}&source={}".format(quote(token),quote(name),quote(str(version)),quote(stage),quote(source))
       r = session.get(url)
       logging.info("Jenkins HTTP return code: {}".format(r.status_code))
