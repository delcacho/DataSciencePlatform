c = get_config()
c.InteractiveShellApp.exec_lines = [
    "from pysparkling import *",
    "import h2o",
    "from pyspark import SparkConf, SparkContext, SparkSession",
    "spark = SparkSession.builder.appName('spark-app').config('spark.driver.port','29413').getOrCreate()",
    "h2oConf = H2OConf(spark).set('spark.ui.enabled', 'false')",
    "hc = H2OContext.getOrCreate(spark, conf=h2oConf)"
]
