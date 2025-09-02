import writer as wf

# This is a placeholder to get you started or refresh your memory.
# Delete it or adapt it as necessary.
# Documentation is available at https://dev.writer.com/framework

# Set environment variables for PySpark (system and version dependent!) 
# if not already set persistently (e.g., in .bashrc or .bash_profile or Windows environment variables)
import os
os.environ["JAVA_HOME"] = "/Library/Internet Plug-Ins/JavaAppletPlugin.plugin/Contents/Home" # Liland's Mac
os.environ["PYSPARK_PYTHON"] = "python" # or similar to "/Users/kristian/miniforge3/envs/tf_M1/bin/python"
os.environ["PYSPARK_DRIVER_PYTHON"] = "python" # or similar to "/Users/kristian/miniforge3/envs/tf_M1/bin/python"
os.environ["PYSPARK_HADOOP_VERSION"] = "without"

# Check how long the following lines take to run
from time import time
start = time()
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('SparkCassandraApp').\
    config('spark.jars.packages', 'com.datastax.spark:spark-cassandra-connector_2.12:3.4.1').\
    config('spark.cassandra.connection.host', 'localhost').\
    config('spark.sql.extensions', 'com.datastax.spark.connector.CassandraSparkExtensions').\
    config('spark.sql.catalog.mycatalog', 'com.datastax.spark.connector.datasource.CassandraCatalog').\
    config('spark.cassandra.connection.port', '9042').getOrCreate()
print("Time taken to run the above lines:", time()-start)
    
# Its name starts with _, so this function won't be exposed
def _update_message(state):
    is_even = state["counter"] % 2 == 0
    message = ("+Even" if is_even else "-Odd")
    state["message"] = message

def decrement(state):
    state["counter"] -= 1
    _update_message(state)

def increment(state):
    state["counter"] += 1
    # Shows in the log when the event handler is run
    print("The counter has been incremented.")
    _update_message(state)
    
# Initialise the state

# "_my_private_element" won't be serialised or sent to the frontend,
# because it starts with an underscore

initial_state = wf.init_state({
    "my_app": {
        "title": "MY APP"
    },
    "_my_private_element": 1337,
    "message": None,
    "counter": 26,
})

_update_message(initial_state)