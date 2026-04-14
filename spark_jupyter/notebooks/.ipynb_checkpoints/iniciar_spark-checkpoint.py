from pyspark.sql import SparkSession

def get_spark(app_name="NotebookPySpark"):
    return (
        SparkSession.builder
        .master("spark://spark-master:7077")
        .appName(app_name)
        .config("spark.driver.host", "spark-notebook")
        .config("spark.driver.bindAddress", "0.0.0.0")
        .config("spark.cores.max", "4")
        .config("spark.executor.cores", "2")
        .config("spark.executor.memory", "1g")
        .config("spark.eventLog.enabled", "true")
        .config("spark.eventLog.dir", "file:///tmp/spark-events")
        .getOrCreate()
    )
# Uso en una celda:
# from iniciar_spark import get_spark
# spark = get_spark("MiNotebook")
# df = spark.range(10)
# df.show()
