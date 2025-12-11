from datetime import datetime

with open("/app/batch_output.txt", "a") as f:
    f.write(f"BATCH JOB RUN AT: {datetime.now()}\n")

print("Batch job executed.")
