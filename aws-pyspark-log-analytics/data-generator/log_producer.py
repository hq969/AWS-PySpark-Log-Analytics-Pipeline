import boto3
import json
from datetime import datetime
import random

kinesis = boto3.client('kinesis', region_name='us-east-1')

def generate_log():
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "ip": f"192.168.1.{random.randint(1, 255)}",
        "method": "GET",
        "endpoint": "/api/v1/data",
        "status": random.choice(["200", "404", "500"])
    }

while True:
    log = generate_log()
    kinesis.put_record(
        StreamName="your-kinesis-stream-name",
        Data=json.dumps(log),
        PartitionKey="partitionKey")
