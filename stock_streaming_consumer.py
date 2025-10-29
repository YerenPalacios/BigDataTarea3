# Este archivo consume datos de acciones desde Kafka y realiza análisis en tiempo real con Spark Streaming
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, from_unixtime, count, avg, max, min
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType

# Crear sesión de Spark con configuración de logging reducido
spark = SparkSession.builder.appName("StockMarketStreaming").getOrCreate()
spark.sparkContext.setLogLevel("WARN")

# Definir el esquema del JSON que llega desde Kafka (debe coincidir exactamente con el producer)
schema = StructType([
    StructField("symbol", StringType()),           # Símbolo de la acción (ej: AAPL, GOOGL)
    StructField("security_name", StringType()),    # Nombre completo de la empresa
    StructField("exchange", StringType()),         # Bolsa donde cotiza
    StructField("market_category", StringType()),  # Categoría de mercado
    StructField("etf", StringType()),              # Indicador si es ETF (Y/N)
    StructField("round_lot_size", DoubleType()),   # Tamaño del lote estándar
    StructField("price", DoubleType()),            # Precio generado aleatoriamente
    StructField("timestamp", IntegerType())        # Timestamp Unix (segundos desde epoch)
])

# Leer stream de datos desde el topic 'stock_data' de Kafka
df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "stock_data")
    .load()
)

# Parsear el JSON del campo 'value' de Kafka y extraer todas las columnas
parsed_df = df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")

# Limpieza de datos: eliminar registros con valores nulos en campos críticos
clean_df = parsed_df.na.drop(subset=["symbol", "security_name", "exchange"])

# Eliminar duplicados basados en el símbolo (opcional, para análisis específicos)
clean_df = clean_df.dropDuplicates(["symbol"])

# Análisis agregado por ventanas de tiempo de 1 minuto para cada símbolo
# Convierte el timestamp Unix a formato timestamp de Spark para usar ventanas temporales
stats = (
    parsed_df
    .withColumn("timestamp_converted", from_unixtime(col("timestamp")).cast("timestamp"))
    .groupBy(window(col("timestamp_converted"), "1 minute"), col("symbol"))
    .agg(
        count("*").alias("num_msgs"),        # Número de mensajes recibidos por símbolo
        avg("price").alias("avg_price"),     # Precio promedio en la ventana
        max("price").alias("max_price"),     # Precio máximo en la ventana
        min("price").alias("min_price")      # Precio mínimo en la ventana
    )
)

# Escribir los resultados en la consola en modo 'complete' (muestra toda la tabla agregada)
query = (
    stats.writeStream
    .outputMode("complete")
    .format("console")
    .start()
)

# Mantener la aplicación corriendo hasta que se interrumpa manualmente
query.awaitTermination()
