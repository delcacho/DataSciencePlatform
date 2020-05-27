from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local").getOrCreate()
from pysparkling import *
import h2o
h2oConf = H2OConf(spark).set('spark.ui.enabled', 'false')
hc = H2OContext.getOrCreate(spark, conf=h2oConf)
print(hc)
