from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .master("spark://192.168.1.12:7077")\
    .appName("LDSA Project") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()

df=spark.read.format("csv").option("header","false").option("delimiter", "\t")\
    .load("/home/ubuntu/DATA/export.tsv")

df.createOrReplaceTempView("Enron")

sqlDF = spark.sql("SELECT _c1 as subject, concat(split(_c2, ' ')[3],'-',split(_c2, ' ')[2],'-', split(_c2, ' ')[1], ' ') as date1 FROM Enron where _c2 like '%:%' order by date1 asc")
