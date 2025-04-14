# AWS PySpark Log Analytics

🔍 Real-time analytics pipeline using AWS + PySpark to analyze server logs.

## ⚙️ Tech Stack
- AWS Kinesis (Log ingestion)
- PySpark on AWS EMR (Streaming processing)
- S3 (Storage)
- Athena + Glue (Query layer)
- Streamlit (Dashboard)

## 📁 Folder Structure
aws-pyspark-log-analytics/ 

├── data-generator/ # Sends fake logs to Kinesis 

├── spark-jobs/ # PySpark job to process logs 

├── config/ # Config files 

├── dashboard/ # Streamlit dashboard 

├── README.md

## 🚀 To Run
1. Deploy Kinesis Stream.
2. Run `data-generator/log_producer.py` to send logs.
3. Submit `streaming_job.py` on AWS EMR.
4. Query output using Athena.
5. Visualize with `streamlit run dashboard/streamlit_app.py`.
