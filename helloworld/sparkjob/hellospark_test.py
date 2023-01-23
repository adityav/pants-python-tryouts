from helloworld.sparkjob import hellospark
import pytest
from pyspark.sql import SparkSession
import os
import sys

@pytest.fixture()
def spark(monkeypatch):
    monkeypatch.setenv("PYSPARK_PYTHON", sys.executable)
    monkeypatch.setenv("PYSPARK_DRIVER_PYTHON", sys.executable)
    spark_session = (SparkSession
        .builder
        .master("local")
        .appName("unit-tests")
        .getOrCreate())
    
    spark_session.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")

    yield spark_session
    spark_session.stop()

def test_hello_job(spark):
    hellospark.hello_spark(spark)