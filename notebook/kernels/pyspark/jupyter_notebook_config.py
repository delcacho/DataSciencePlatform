c = get_config()
c.InteractiveShellApp.exec_lines = [
    "from dask.distributed import Client",
    "client = Client('scheduler:8786')",
    "import os",
    "os.environ['MODIN_ENGINE'] = 'dask'",
    "import modin.pandas as pd",
    "from pyspark import SparkConf, SparkContext",
    "spark = SparkSession.builder.appName('spark-app').config('spark.driver.port','29413').getOrCreate()",
    "sc = spark.sparkContext"
]
