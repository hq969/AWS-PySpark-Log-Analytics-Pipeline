# AWS PySpark Log Analytics

🔍 Real-time analytics pipeline using AWS + PySpark to analyze server logs.

## ⚙️ Tech Stack
- AWS Kinesis (Log ingestion)
- PySpark on AWS EMR (Streaming processing)
- S3 (Storage)
- Athena + Glue (Query layer)
- Streamlit (Dashboard)

## 📁 Folder Structure 

```
aws-pyspark-log-analytics/
├── README.md               # Project overview and setup guide
├── data-generator/         # Python script to simulate and send logs to Kinesis
│   └── send_logs.py

├── spark-jobs/             # PySpark ETL job for processing real-time logs
│   └── process_logs.py

├── config/                 # Configuration files for stream, batch jobs, and schema
│   └── kinesis_config.json

├── dashboard/              # Streamlit dashboard for visualizing processed logs
│   └── app.py

```

## 🚀 To Run
1. Deploy Kinesis Stream.
2. Run `data-generator/log_producer.py` to send logs.
3. Submit `streaming_job.py` on AWS EMR.
4. Query output using Athena.
5. Visualize with `streamlit run dashboard/streamlit_app.py`.
