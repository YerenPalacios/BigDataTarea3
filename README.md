# Stock Market Streaming con Kafka y Spark

Proyecto de Big Data que simula el procesamiento en tiempo real de datos del mercado de valores utilizando Apache Kafka como sistema de mensajería y Apache Spark Streaming para el análisis de datos.

## 📋 Descripción

Este proyecto consta de dos componentes principales:

1. **Producer (`stock_producer.py`)**: Lee datos de un dataset de acciones de Kaggle y envía información aleatoria de precios a un topic de Kafka cada segundo.

2. **Consumer (`stock_streaming_consumer.py`)**: Consume los datos desde Kafka usando Spark Streaming y realiza análisis agregados por ventanas de tiempo de 1 minuto, calculando estadísticas como precio promedio, máximo y mínimo por símbolo.

## 🔧 Requisitos Previos

### Software Necesario

- **Apache Kafka** (instalado en `/opt/Kafka/`)
- **Apache Spark** 4.0.1 o superior
- **Python 3.x**
- **Java** (requerido por Kafka y Spark)

### Librerías Python

```bash
pip install kafka-python pandas pyspark
```

## 🚀 Instrucciones de Ejecución

### 1. Iniciar Zookeeper

```bash
sudo /opt/Kafka/bin/zookeeper-server-start.sh /opt/Kafka/config/zookeeper.properties &
```

### 2. Iniciar Servidor Kafka

```bash
sudo /opt/Kafka/bin/kafka-server-start.sh /opt/Kafka/config/server.properties &
```

### 3. Crear el Topic

```bash
/opt/Kafka/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic stock_data
```

**Nota:** Si el topic ya existe, este paso puede omitirse.

### 4. Ejecutar el Producer

```bash
python3 stock_producer.py
```

Este script comenzará a enviar datos de acciones a Kafka cada segundo.

### 5. Ejecutar el Consumer (en otra terminal)

```bash
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.13:4.0.1 stock_streaming_consumer.py
```

El consumer mostrará en consola estadísticas agregadas por ventanas de 1 minuto.

## 📊 Datos Procesados

El sistema procesa la siguiente información por cada acción:

- **Symbol**: Símbolo de la acción (ej: AAPL, GOOGL)
- **Security Name**: Nombre completo de la empresa
- **Exchange**: Bolsa donde cotiza
- **Market Category**: Categoría de mercado
- **ETF**: Indicador si es ETF (Y/N)
- **Round Lot Size**: Tamaño del lote estándar
- **Price**: Precio generado aleatoriamente (simulación)
- **Timestamp**: Marca de tiempo Unix

## 🔍 Análisis Realizado

El consumer realiza las siguientes operaciones:

1. **Limpieza de datos**: Elimina registros con valores nulos
2. **Deduplicación**: Elimina duplicados por símbolo
3. **Agregaciones por ventana temporal** (1 minuto):
   - Número de mensajes recibidos
   - Precio promedio
   - Precio máximo
   - Precio mínimo

## 📝 Dataset

El proyecto utiliza el dataset [Stock Market Dataset](https://www.kaggle.com/datasets/jacksoncrow/stock-market-dataset) de Kaggle, que se descarga automáticamente al ejecutar el producer.

## ⚠️ Notas

- Asegúrate de que los puertos 2181 (Zookeeper) y 9092 (Kafka) estén disponibles
- El producer genera precios aleatorios entre 10 y 500 para simulación
- Para detener los procesos, usa `Ctrl+C` en cada terminal


