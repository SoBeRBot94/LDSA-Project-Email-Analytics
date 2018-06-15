from pyspark.sql import SparkSession
import re
spark_session = SparkSession.builder.master("spark://192.168.1.12:7077").getOrCreate()
#only keep emails that have the following fields
p1 = re.compile('MESSAGE-ID:', re.IGNORECASE)
p2 = re.compile('Subject:', re.IGNORECASE)
p3 = re.compile('Date:', re.IGNORECASE)

spark_context = spark_session.sparkContext
#read the emails
rdd_all = spark_context.wholeTextFiles('/home/ubuntu/DATA/enron_mail_20110402/maildir/*/all_documents/*').cache()
def f1(l):
    m= ""
    s= ""
    d= ""
    for v in l:
        if v.startswith("Message-ID:"):
            m=v.strip("Message-ID: ")
        elif v.startswith("Subject:"): 
            s=v.strip("Subject: ")
        elif v.startswith("Date"):
            d=v.strip("Date: ")
    return [m,s,d] 
    
#get subjects and date from distinct emails
lines = rdd_all.filter(lambda doc: bool(p1.search(doc[1])) & bool(p2.search(doc[1])) & bool(p3.search(doc[1]))).map(lambda filename_content: filename_content[1].split('\r\n\r\n')[0]).map(lambda x: x.split('\r\n')).map(f1).collect()

with open("export.tsv", 'w') as tsvwrite:
	for line in lines:
		tsvwrite.write('\t'.join(line)+'\n')

