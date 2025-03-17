from pyspark.sql import SparkSession
from pyspark.sql.functions import col

def clean_data():
    spark = SparkSession.builder \
        .appName("Data Processing") \
        .config("spark.mongodb.input.uri", "mongodb://localhost:27017/GOLLO.PRODUCTOS_GOLLO") \
        .config("spark.mongodb.output.uri", "mongodb://localhost:27017/GOLLO.PRODUCTOS_GOLLO") \
        .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
        .config("spark.hadoop.io.nativeio.NativeIO$Windows", "false") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("ERROR")

    df = spark.read.format("mongo").load()

    df = df.dropDuplicates()
    df = df.na.fill({'PRECIO_ACTUAL': 0, 'PRECIO_ORIGINAL': 0, 'PERC_DESCUENTO': 0.0})

    df = df.withColumn("PRECIO_ACTUAL", col("PRECIO_ACTUAL").cast("double"))
    df = df.withColumn("PRECIO_ORIGINAL", col("PRECIO_ORIGINAL").cast("double"))
    df = df.withColumn("PERC_DESCUENTO", col("PERC_DESCUENTO").cast("double"))
    
    df.show()

    df = df.drop("_id")

    try:
        df.coalesce(1).write.mode('overwrite').options(header='True', delimiter=',').csv("output/processed_data.csv")

    except Exception as e:
        print(f"Error al escribir el archivo CSV: {e}")

    print("Procesamiento completado.")
    return df.toPandas()

if __name__ == "__main__":
    print(clean_data())