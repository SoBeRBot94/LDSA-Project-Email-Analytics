from pyspark.sql import SparkSession

spark_session = SparkSession\
        .builder\
        .master("spark://192.168.1.12:7077") \
        .config('spark.executor.memory', '2g') \
        .appName("project11")\
        .getOrCreate()

spark_context = spark_session.sparkContext

rdd = spark_context.textFile("/home/ubuntu/DATA/enron_mail_20110402/maildir/king-j/all_documents/1.")

#('/home/ubuntu/DATA/enron_mail_20110402/maildir/*/all_documents/*', minPartitions=40)
dataframe = spark_session.read.load("/home/ubuntu/DATA/enron_mail_20110402/maildir/king-j/all_documents/1.", format="csv").cache()

#spark_context.stop()

dataframe.head(5)

#The 5 top rows are the ones we need for solving the assignment
