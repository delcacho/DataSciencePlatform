FROM python:3.6.10

# We need to install the following dependencies explicitly:
# - psycopg2-binary to work with a Postgres-backed backend store
RUN pip install psycopg2-binary==2.8.4 && \   
    pip install mlflow[extras]==1.8.0

ENTRYPOINT ["mlflow", "server"]
