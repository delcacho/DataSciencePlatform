import json
import requests
import logging
from urllib.parse import quote
from confluent_kafka import Consumer, KafkaException
from sqlalchemy import create_engine

def getRunIdFromSource(source):
   # s3://clusters.dev.bayescluster.com/mlruns/1/22f86133a05344f099c580a453c386b5/artifacts/wine
   pos = source.find("/mlruns/") + len("/mlruns/")
   start = source.find("/",pos)
   end = source.find("/",start+1)
   return source[(start+1):end]
   
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
             dbstr = 'postgres://postgres:pruebademlflow@postgres-postgresql-headless.default.svc.cluster.local:5432/mlflowdb'
             try:
                db = create_engine(dbstr)
                run_id = getRunIdFromSource(source)
                result_set = db.execute("SELECT value FROM tags WHERE key='replicas' and run_uuid='{}'".format(run_id))
                row = result_set.fetchone()
                replicas = row[0] if row is not None else '1'
             except:
                replicas = '1'
                pass
             finally:
                db.dispose()
             logging.info("Going to launch Jenkins job: name={}, version={}, stage={}, source={}".format(name,version,stage,source))
             url = "http://jenkins:8080/job/SeldonDeployer/buildWithParameters?token={}"\
                   "&name={}&version={}&stage={}&source={}&replicas={}".format(quote(token),quote(name),quote(str(version)),quote(stage),quote(source),quote(str(replicas)))
             session = requests.Session()
             session.auth = (user, password)
             r = session.get(url)
             logging.info("Jenkins HTTP return code: {}".format(r.status_code))
   except Exception as e:
      logging.error("Exception received: {}",e)
