c = get_config()
c.InteractiveShellApp.exec_lines = [
    "from pyspark import SparkConf",
    "from pyspark.sql import SparkSession",
    "from pyspark import SparkContext",
    "from dask.distributed import Client",
    "import h2o",
    "conf = SparkConf()",
    "conf.set('spark.driver.port','29413')",
    "conf.set('spark.sql.repl.eagerEval.enabled', True)",
    "spark = SparkSession.builder.config(conf=conf).getOrCreate()",
    "sc = spark.sparkContext",
    "from pysparkling import *",
    "h2oConf = H2OConf(spark).set('spark.ui.enabled', 'false')",
    "hc = H2OContext.getOrCreate(spark, conf=h2oConf)"
]
