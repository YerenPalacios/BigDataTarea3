# Este archivo lee la información del dataset y cada segundo la envia a kafka
import time
import json
import os
import random
import pandas as pd
from kafka import KafkaProducer
import kagglehub

# Carga del dataset
# 1️⃣ Descargar dataset de Kaggle
path = kagglehub.dataset_download("jacksoncrow/stock-market-dataset")
print("Dataset descargado en:", path)

# Leer el archivo CSV específico del dataset
csv_file = os.path.join(path, "symbols_valid_meta.csv")
df = pd.read_csv(csv_file)

# Configuración del producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

while True:
    # Tomar una fila aleatoria del dataset
    row = df.sample(1).iloc[0]
    data = {
        "symbol": row["Symbol"],
        "security_name": row["Security Name"],
        "exchange": row["Listing Exchange"],
        "market_category": row["Market Category"],
        "etf": row["ETF"],
        "round_lot_size": row["Round Lot Size"],
        "price": round(random.uniform(10, 500), 2),
        "timestamp": int(time.time())
    }
    producer.send("stock_data", value=data)
    print(f"Sent: {data}")
    time.sleep(1)
