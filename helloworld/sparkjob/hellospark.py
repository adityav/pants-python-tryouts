from pyspark.sql import SparkSession
import pandas as pd
from pyspark.sql.functions import pandas_udf

def hello_spark(spark: SparkSession):
    """Hello world spark!"""
    
    @pandas_udf("double") # type: ignore
    def mean_udf(v: pd.Series) -> float:
        return v.mean()
    
    df = spark.createDataFrame(
        [(1, 1.0), (1, 2.0), (2, 3.0), (2, 5.0), (2, 10.0)],
        ("id", "v"))

    print(df.groupby("id").agg(mean_udf(df['v'])).collect())


if __name__ == "__main__":
    hello_spark(SparkSession.builder.getOrCreate())