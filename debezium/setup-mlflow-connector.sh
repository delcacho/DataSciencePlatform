curl -v -X POST \
  http://kafkaconnect-service:8083/connectors \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "containers-connector",
    "config": {
            "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
            "plugin.name": "pgoutput",
            "database.hostname": "postgres-postgresql-headless.default.svc.cluster.local",
            "database.port": "5432",
            "database.user": "postgres",
            "database.password": "pruebademlflow",
            "database.dbname": "mlflowdb",
            "database.server.name": "postgres",
            "table.whitelist": "public.model_versions"
      }
}'
