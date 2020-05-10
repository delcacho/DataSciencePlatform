c = get_config()
c.InteractiveShellApp.exec_lines = [
    "from pysparkling import *",
    "import h2o",
    "from pyspark import SparkConf, SparkContext",
    "from pyspark.sql import SparkSession",
    "h2oConf = H2OConf(spark).set('spark.ui.enabled', 'false')",
    "hc = H2OContext.getOrCreate(spark, conf=h2oConf)"
]
