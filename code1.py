from pyspark.sql import SparkSession

spark_session = SparkSession\
        .builder\
        .master("spark://192.168.1.12:7077") \
        .config('spark.executor.memory', '2g') \
        .appName("project11")\
        .getOrCreate()

spark_context = spark_session.sparkContext

rdd = spark_context.textFile("/home/ubuntu/DATA/enron_mail_20110402/maildir/king-j/all_documents/1.")
