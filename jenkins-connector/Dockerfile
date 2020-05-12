FROM continuumio/miniconda3:4.7.12

RUN pip install kafka-python

RUN mkdir -p /usr/local/bin/jenkins-connector
COPY connector.py /usr/local/bin/jenkins-connector/connector.py

RUN conda install --yes \
    -c conda-forge \
    tini==0.18.0

COPY prepare.sh /usr/bin/prepare.sh

ENTRYPOINT ["tini", "-g", "--", "/usr/bin/prepare.sh"]
