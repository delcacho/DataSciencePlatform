FROM continuumio/miniconda3:4.7.12

RUN conda install python=3.6.9

RUN pip install -U kafka-python requests confluent-kafka

RUN mkdir -p /usr/local/bin/jenkins-connector
COPY connector.py /usr/local/bin/jenkins-connector/connector.py

CMD ["python3", "/usr/local/bin/jenkins-connector/connector.py"]
