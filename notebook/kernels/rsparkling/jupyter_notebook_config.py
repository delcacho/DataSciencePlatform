c = get_config()
c.InteractiveShellApp.exec_lines = [
    "library(sparklyr)",
    "sc <- spark_connect('spark://spark-master-svc:7077')"
]
