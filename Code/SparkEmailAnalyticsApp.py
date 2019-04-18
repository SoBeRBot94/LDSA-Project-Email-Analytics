#!/usr/bin/env python3

from pyspark.sql import SparkSession
import re
import yaml

def config():
    with open('/home/ubuntu/SparkApp/sparkAppConfig.yml', 'r') as configFile:
        config = yaml.load(configFile)

    masterURL = config['sparkContext']['masterURL']
    appName = config['sparkContext']['appName']
    basePath = config['input']['basePath']
    partitions = config['input']['partitions']
    outFile = config['export']['csvFile']

    return masterURL, appName, basePath, partitions, outFile

masterURL, appName, basePath, partitions, outFile = config()

def sparkSessionBuilder():
    spark = SparkSession.builder.appName(appName).master(masterURL).getOrCreate() 
    '''Initialize Spark Entrypoint'''

    return spark

spark = sparkSessionBuilder()

def sparkContextBuilder():
    sc = spark.sparkContext

    return sc

sc = sparkContextBuilder()

def RDDHeadersStripper(lines):
    '''Function to Strip Headers'''

    messageID = ""
    From = ""
    date = ""
    
    for values in lines:
        if values.startswith("Message-ID:"):
            messageID = values.strip("Message-ID: ")
        elif values.startswith("From:"):
            From = values.strip("From: ")
        elif values.startswith("Date:"):
            date = values.strip("Date: ")
    
    return [messageID, subject, date]

def RDDBuilder():
    inputRDD = sc.wholeTextFiles(basePath + "/" + "text_000" + "/*", partitions).cache()
    '''Read All The Files From sent_items Directory'''

    filteredRDD = inputRDD.filter(lambda x: bool(re.compile('MESSAGE-ID:', re.IGNORECASE).search(x[1])) & bool(re.compile('From:', re.IGNORECASE).search(x[1])) & bool(re.compile('Date:', re.IGNORECASE).search(x[1]))).map(lambda x: x[1].strip('\r\n\r\n')[0]).map(lambda x: x.split('\r\n')).map(RDDHeadersStripper).collect()

    return filteredRDD

filteredRDD = RDDBuilder()

with open(outFile, 'w') as CSVFile:
    for lines in filteredRDD:
        CSVFile.write(','.join(lines)+'\n')
