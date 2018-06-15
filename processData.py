#!/usr/bin/env python3

import pyspark as pys
sparkC = pys.SparkContext()

from pyspark.sql import SparkSession

sparkS = SparkSession.builder.appName("LDSA Email Analytics").config("spark.some.config.option", "some-value").getOrCreate()

inputDataframe=sparkS.read.format("csv").option("header", "false").option("delimiter", "\t").load("file:///home/ubuntu/export.tsv")
inputDataframe.createOrReplaceTempView("Enron_initial")

intermediateDataframe = sparkS.sql("SELECT _c0 as messageIds, concat(split(_c2, ' ')[3]) as Year FROM Enron_initial where _c2 like '%:%' order by Year asc")
intermediateDataframe.createOrReplaceTempView("Enron_intermediate")

outputDataframe = sparkS.sql("SELECT count(messageIds) as No_of_Messages, Year as Year from Enron_intermediate group by Year").take(7)

with open('Counts.txt', 'w') as outputFile:
    for row in outputDataframe:
        outputFile.write(str(row) + "\n")
