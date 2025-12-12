````markdown
# Simplified Data Monitoring Platform (Stream + Batch)

This simplified project provides a minimal, easy-to-understand data platform that demonstrates:
- collection/monitoring (Prometheus + node_exporter)
- alerting (Alertmanager -> webhook)
- visualization (Grafana)
- stream processing (Kafka, stream-processor)
- batch processing (batch-processor writing timestamps)

Quick start (from repository root):

cd data-monitoring-platform
# build and start all services
docker-compose up -d --build

Wait a minute for services to initialize.

Check UIs:
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/admin)
- Alertmanager: http://localhost:9093
- Kafdrop: http://localhost:9000
- Alert webhook (optional check): http://localhost:5001

Test alert routing (PowerShell on Windows):
$ts = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ssZ")
$json = "[{\"labels\":{\"alertname\":\"ManualTest\",\"severity\":\"critical\"},\"annotations\":{\"summary\":\"Manual test alert\"},\"startsAt\":\"$ts\"}]"
Invoke-RestMethod -Uri 'http://localhost:9093/api/v2/alerts' -Method Post -Body $json -ContentType 'application/json'

Verify Alertmanager received the alert:
Invoke-RestMethod -Uri 'http://localhost:9093/api/v2/alerts' -Method Get

Test stream processing (send a single message to Kafka):
# Use a temporary Python container on the same network
NETWORK_NAME=$(docker network ls --filter name=monitor-net -q | xargs -n1 docker network inspect --format '{{.Name}}' )
# If the above is empty, use the compose network name printed by "docker network ls"

docker run --rm --network $NETWORK_NAME python:3.10-slim sh -c "pip install kafka-python && python - <<'PY'\nfrom kafka import KafkaProducer\np=KafkaProducer(bootstrap_servers='kafka:9092')\np.send('raw_data', b'hello-from-test')\np.flush()\nprint('sent')\nPY"

Check the stream processor logs:
docker logs -f stream_processor

Check that processed message exists by consuming 'processed_data' topic similarly.

Batch processor:
- The batch_processor service writes a timestamp every 5 minutes to /data/batch_output.txt inside the container.
- To inspect logs: docker logs -f batch_processor
- To persist output to host, run the container with a bind mount (optional).

Defendable points to discuss during the project defense:
- Architecture choices: why Kafka for stream processing and periodic batch for batch jobs.
- How monitoring and alerting are connected (Prometheus rules -> Alertmanager -> webhook).
- How to extend the platform: persistence (TimescaleDB/ClickHouse), auth, production-grade security, scalability.

If you want, I can:
- Add a mount to persist batch output to the host.
- Add a simple consumer test script to the repo.
- Remove the AlwaysFiring test rule before submission.
````
