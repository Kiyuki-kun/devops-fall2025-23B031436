import time
from datetime import datetime

print('Batch processor started. It will write a timestamp every 5 minutes to /data/batch_output.txt')

# Write to /data so users can mount a volume if desired
output_file = '/data/batch_output.txt'

while True:
    ts = datetime.utcnow().isoformat() + 'Z'
    line = f'BATCH RUN AT {ts}\n'
    try:
        with open(output_file, 'a') as f:
            f.write(line)
        print('Wrote:', line.strip())
    except Exception as e:
        print('Failed to write batch output:', e)
    time.sleep(300)  # 5 minutes
