
from pyspark import SparkConf,SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import Row,SQLContext
import sys
import requests
import pandas as pd

def load_wordlist(filename):
    file = open(filename,'rU')
    words = set(line.strip() for line in file)
    return words

pwords = load_wordlist("positive.txt")
nwords = load_wordlist("negative.txt")


def orientation(sentence,pwords,nwords):
    counter = 0
    word = sentence.split()
    for i in word:
        if i in nwords:
            counter = counter + 1
        elif i in pwords:
            counter = counter - 1
    return (word[0],counter)

def aggregate_tags_count(new_values, total_sum):
    return sum(new_values) + (total_sum or 0)

def get_sql_context_instance(spark_context):
    if ('sqlContextSingletonInstance' not in globals()):
        globals()['sqlContextSingletonInstance'] = SQLContext(spark_context)
    return globals()['sqlContextSingletonInstance']

def process_rdd(time, rdd):
    print("----------- %s -----------" % str(time))
    try:
        sql_context = get_sql_context_instance(rdd.context)
        row_rdd = rdd.map(lambda w: Row(tweet_user=w[0], feeling_count=w[1]))
        feelings_df = sql_context.createDataFrame(row_rdd)
        feelings_df.registerTempTable("feelings")
        feeling_counts_df = sql_context.sql("select tweet_user, feeling_count from feelings order by feeling_count desc")
        feeling_counts_df.show()
        feeling_pandas = feeling_counts_df.toPandas()
        feeling_pandas.to_csv('user_feeling.csv', header=True, index=True)
        #feeling_counts_df.repartition(1).write.format('com.databricks.spark.csv').save("/data/home/alfonso.villegas/myfile.csv",header = 'true')
        #feeling_counts_df.write.format('com.databricks.spark.csv').save("/data/home/alfonso.villegas/feelings.csv")
    except:
        e = sys.exc_info()[0]
        print("No Relevant Data")

# create spark configuration
conf = SparkConf()
conf.setAppName("TwitterStreamApp")

# create spark context with the above configuration
sc = SparkContext()
sc.setLogLevel("ERROR")
# create the Streaming Context from the above spark context with interval size 5 seconds
ssc = StreamingContext(sc, 5)

# setting a checkpoint to allow RDD recovery
ssc.checkpoint("my_checkpoint")

# read data from the port
lines = ssc.socketTextStream("localhost", 9595)

# filters tweets to get only the ones with Verizon
verizon_tweet = lines.filter(lambda s: 'Verizon' in s or 'verizon' in s or '@Verizon' in s or '@VerizonSupport' in s)
    # Each element of verizon_tweet will be the text of a tweet.
    # You need to find the count of all the positive and negative words in these tweets.
    # Keep track of a running total counts and print this at every time step (use the pprint function).
    #word = verizon_tweet.flatMap(lambda k: k.split(" "))
wordsType = verizon_tweet.map(lambda k: orientation(k,pwords,nwords))

    #count = wordsType.reduceByKey(lambda a, b : a + b)
    # Let the counts variable hold the word counts for all time steps
    # You will need to use the foreachRDD function.
    # For our implementation, counts looked like:
    #   [[("positive", 100), ("negative", 50)], [("positive", 80), ("negative", 60)], ...]

cts = wordsType.updateStateByKey(aggregate_tags_count)
cts.pprint()
cts.foreachRDD(process_rdd)

# start the streaming computation
ssc.start()
# wait for the streaming to finish
ssc.awaitTermination()
