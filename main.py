import subprocess
import time


def wait_for_postgres(host, max_retries=5, delay_seconds=5):
    for attempt in range(1, max_retries + 1):
        try:
            result = subprocess.run(
                ["pg_isready", "-h", host],
                check=True,
                capture_output=True,
                text=True
            )
            if "accepting connections" in result.stdout:
                print(f"[INFO] PostgreSQL at {host} is ready.")
                return True
        
            except subprocess.CalledProcessError:
            print(f"[WARN] PostgreSQL not ready on attempt {attempt}/{max_retries}. Retrying in {delay_seconds}s...")
            time.sleep(delay_seconds)
