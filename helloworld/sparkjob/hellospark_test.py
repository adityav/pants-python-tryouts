from helloworld.sparkjob import hellospark
import pytest
from pyspark.sql import SparkSession

@pytest.fixture()
def spark():
    spark_session = (SparkSession
        .builder
        .master("local")
        .appName("unit-tests")
        .getOrCreate())
    
    yield spark_session
    spark_session.stop()

def test_hello_job(spark):
    hellospark.hello_spark(spark)