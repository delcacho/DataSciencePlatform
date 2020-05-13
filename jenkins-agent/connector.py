import json
import requests
import logging
from urllib.parse import quote
from confluent_kafka import Consumer, KafkaException

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

conf = {'bootstrap.servers': 'kafka:9092', 'group.id': 'mlflow-group', 
        'session.timeout.ms': 6000, 'auto.offset.reset': 'earliest',
        'enable.auto.commit': True, 'session.timeout.ms': 6000}

logging.info("Connecting to Kafka queue...")
consumer = Consumer(conf)

def print_assignment(consumer, partitions):
        print('Assignment:', partitions)

# Subscribe to topics
logging.info("Subscribing to topic...")
consumer.subscribe(['postgres.public.model_versions'], on_assign=print_assignment)

token = "gundisalvo"
user = "admin"
password = "11ee1c7cb4a9daf80133c23476e2fa3fc0"


logging.info("Starting polling loop...")
while True:
   try:
      msg = consumer.poll(timeout=1.0)
      if msg is None:
          continue
      if msg.error():
          raise KafkaException(msg.error())
      else:
          message = json.loads(msg.value().decode('utf8'))
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
             session = requests.Session()
             session.auth = (user, password)
             r = session.get(url)
             logging.info("Jenkins HTTP return code: {}".format(r.status_code))
   except Exception as e:
      logging.error("Exception received: {}",e)
