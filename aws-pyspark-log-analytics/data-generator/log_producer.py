import boto3
import json
import time
import random
from datetime import datetime

kinesis = boto3.client('kinesis', region_name='us-east-1')
stream_name = 'your-kinesis-stream-name'

def generate_log():
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "ip": f"192.168.0.{random.randint(1, 255)}",
        "method": random.choice(["GET", "POST", "DELETE"]),
        "endpoint": random.choice(["/login", "/signup", "/api/data", "/logout"]),
        "status": random.choice(["200", "404", "500", "403"])
    }

while True:
    log = generate_log()
    print("Sending log:", log)
    kinesis.put_record(
        StreamName=stream_name,
        Data=json.dumps(log),
        PartitionKey="partitionKey")
    time.sleep(1)  # simulate 1 request/sec
